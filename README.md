# Evolve (EWB!) super pom

The super pom for Zepben apps.

## Updating

While the major version is <1.0.0, changes should bump the minor (y in x.y.z) version number manually
(CI does not do this automatically like other Zepben repos).
If you have fixed a bug in the pom you can probably just increment the z number, but while
we are less than 1.0.0 it probably doesn't make much difference...

## Building pipeline-java-ewb container

We build the `pipeline-java-ewb` container after releasing a new superpom, or on demand. The reason for this container is to
include a Maven repository with as many dependencies as possible, so that our actual Maven builds are quicker.

There are 3 ways that this container is built:

 1. Automatically for superpom releases via a series of flows dispatches. In this case, we want to only update the current repository with new packages/versions, preserving all the packages that are already there. This allows us to cache packages for many superpom releases in the same repository.

 2. Automatically for rebasing on a newer `pipeline-java` container to include fixes and updates to ci-utils/tools. In this case we only want to rebase the current container image on top of a new one.

 3. Manually, by providing an initial commit; then a new container is build via a series of steps by checking out all the commits starting with the provided SHA and ending on HEAD. Can be used in cases where the container gets too big by carrying old and unnecessary dependencies and we want to start afresh.

 The container might also be built for the PR checks, but only to test the build process, i.e without pushing it to a repository.
