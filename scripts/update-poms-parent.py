import subprocess
import tempfile
import sys
from enum import Enum, auto
from getpass import getpass
from multiprocessing.pool import ThreadPool
from typing import List
from typing import NamedTuple

import requests


class Repo(NamedTuple):
    name: str
    srcref: str
    cloneref: str


class Auth(NamedTuple):
    user: str
    password: str


class UpdateVersionError(Exception):
    class Type(Enum):
        GIT_ERROR = auto()
        UPDATE_PARENT_FAILED = auto()
        BUILD_FAILED = auto()

    def __init__(self, type: Type, repo_name: str, cmd: str, return_code: int, err: str):
        super().__init__()
        self.type = type
        self.repo_name = repo_name
        self.cmd = cmd
        self.return_code = return_code
        self.err = err

    def __str__(self):
        return str({
            "repo": self.repo_name,
            "type": str(self.type),
            "cmd": self.cmd,
            "code": self.return_code,
            "err": (self.err[:252] + '...') if len(self.err) > 252 else self.err
        })


class ProcessRepo:
    class Result(NamedTuple):
        name: str
        match: bool = False
        changed: bool = False
        err: UpdateVersionError = None

    def __init__(self, repo: Repo, auth: Auth, test_run: bool = False):
        self.auth = auth
        self.repo = repo
        self.wd = tempfile.TemporaryDirectory(prefix=repo.name.replace(" ", "_") + "_")
        self.test_run = test_run

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.wd.cleanup()

    def process(self) -> Result:
        git_dir = self.wd.name
        pom_path = git_dir + "/pom.xml"
        repo_name = self.repo.name

        try:
            cmd = ["git", "clone", self.repo.cloneref + "/master", git_dir]
            self._run_fatal_cmd(cmd, repo_name, UpdateVersionError.Type.GIT_ERROR)

            cmd = ["mvn", "-f", pom_path, "versions:update-parent", "-DallowSnapshots=true",
                   "-DgenerateBackupPoms=false"]
            self._run_fatal_cmd(cmd, repo_name, UpdateVersionError.Type.UPDATE_PARENT_FAILED)

            changed = self._has_changes(git_dir)
            if changed:
                if not self.test_run:
                    cmd = ["git", "-C", git_dir, "add", "."]
                    self._run_fatal_cmd(cmd, repo_name, UpdateVersionError.Type.GIT_ERROR)

                    cmd = ["git", "-C", git_dir, "commit", "-m", "'Updated parent in poms'"]
                    self._run_fatal_cmd(cmd, repo_name, UpdateVersionError.Type.GIT_ERROR)

                    cmd = ["git", "-C", git_dir, "push"]
                    self._run_fatal_cmd(cmd, repo_name, UpdateVersionError.Type.GIT_ERROR)

                # We still want to commit and push the updated version,
                # but we run the tests so we can report any issues if the tests now fail
                cmd = ["mvn", "-f", pom_path, "clean", "test"]
                self._run_fatal_cmd(cmd, repo_name, UpdateVersionError.Type.BUILD_FAILED)
        except UpdateVersionError as err:
            return ProcessRepo.Result(repo_name, match=True, err=err)

        return ProcessRepo.Result(self.repo.name, match=True, changed=changed)

    @staticmethod
    def _has_changes(git_dir: str) -> bool:
        cmd = ["git", "-C", git_dir, "diff-index", "--quiet", "HEAD", "--"]
        return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0

    @staticmethod
    def _run_fatal_cmd(cmd: List[str], name: str, error_type: UpdateVersionError.Type):
        try:
            proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            proc.check_returncode()
        except subprocess.CalledProcessError as err:
            raise UpdateVersionError(error_type, name, " ".join(cmd), err.returncode, str(err.stderr))


class PomParentVersionUpdater:
    def __init__(self, bitbucket_user: str, auth: Auth, test_run: bool = False):
        self.user = bitbucket_user
        self.auth = auth
        self.pool = ThreadPool(processes=4)
        self.test_run = test_run

    def process_repos(self):
        futures = self._run_updates()
        self._report_results(futures)

    def _run_updates(self):

        # Method to pass to the thread pool to kick off the update process
        def process_repo(r: Repo, auth: Auth) -> ProcessRepo.Result:
            if self._is_maven_repo(r):
                with ProcessRepo(r, auth, test_run = self.test_run) as processor:
                    return processor.process()

            return ProcessRepo.Result(r.name)

        next_url = 'https://api.bitbucket.org/2.0/repositories/' + self.user
        fix this to only update company super pom projects, not ednar projects
        futures = []
        while next_url:
            response = self.__get_repos_page(next_url)
            if response.status_code != 200:
                msg = "Unable to get repo list, some repos will not be updated. [url: {}, status: {}]."
                print(msg.format(next_url, response.status_code))
                next_url = None
                continue

            response_json = response.json()
            for value in response_json["values"]:
                repo = self._get_repo_links(value)
                future = self.pool.apply_async(process_repo, (repo, self.auth))
                futures.append(future)

            next_url = response_json.get("next")

        return futures

    def _report_results(self, futures):
        bad = []
        for future in futures:
            result = future.get()
            if result.match:
                if result.changed:
                    print("Updated pom parent for " + result.name)
                elif result.err:
                    msg = "Failed to update pom parent for {}: {}".format(result.name, str(result.err))
                    if not self.test_run:
                        if not self._create_jira_issue(result.err):
                            msg += "\nFailed to create JIRA task for failed update of " + result.name

                    bad.append(msg)
                else:
                    print(result.name + " is already updated")

        for msg in bad:
            print(msg)

    def _is_maven_repo(self, repo: Repo) -> bool:
        url = repo.srcref + "/master/pom.xml"
        response = requests.get(url, auth=self.auth)
        return response.status_code == 200

    def __get_repos_page(self, url: str) -> requests.Response:
        return requests.get(url, auth=self.auth)

    @staticmethod
    def _get_repo_links(repo_json) -> Repo:
        name = repo_json["name"]
        srcref = repo_json["links"]["source"]["href"]
        cloneref = [clone["href"] for clone in repo_json["links"]["clone"] if clone["name"] == "https"][0]
        return Repo(name, srcref, cloneref)

    def _create_jira_issue(self, error: UpdateVersionError) -> bool:
        summary = "Failed to update pom parent for " + error.repo_name
        desc = "Failed to update pom parent for {}.\n\nCommand '{}' exited with status code {}\n\n{}".format(
            error.repo_name,
            error.cmd,
            error.return_code,
            (error.err[:1000] + '...') if len(error.err) > 1000 else error.err)

        body = {
            "fields": {
                "project": {
                    "key": "ERIS"
                },
                "summary": summary,
                "description": desc,
                "issuetype": {
                    "name": "Bug"
                },
                "priority": {
                    "name": "Highest"
                }
            }
        }

        url = "https://{}.atlassian.net/rest/api/2/issue".format(self.user)
        response = requests.post(url, auth=self.auth, json=body)
        return response.status_code == 200


if __name__ == "__main__":
    test = "--test" in sys.argv
    if test:
        print("Running in test mode. No commits will be made.")

    user = input("Enter Atlassian ID: ")
    if user.find("@") == -1:
        user = user + "@zepben.com"
        print("No @ found in user, making user " + user)
    passwd = getpass()
    PomParentVersionUpdater("zepben", Auth(user, passwd), test_run=test).process_repos()
