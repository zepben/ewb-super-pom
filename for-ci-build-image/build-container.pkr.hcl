packer {
  required_plugins {
    docker = {
      source  = "github.com/hashicorp/docker"
      version = "~> 1"
    }
  }
}

variable "dockerhub_pw" {
  type    = string
  default = "${env("DOCKER_HUB_ACCESS_TOKEN")}"
}

variable "dockerhub_user" {
  type    = string
  default = "${env("DOCKER_HUB_USER")}"
}

source "docker" "image" {
  commit = "true"
  image  = "maven:3.9.8-amazoncorretto-11-al2023"
}

build {
  sources = ["source.docker.image"]

  provisioner "file" {
    destination = "/root/deps-pom.xml"
    source      = "../deps-pom.xml"
  }

  provisioner "file" {
    destination = "/root/pom.xml"
    source      = "../pom.xml"
  }

  provisioner "file" {
    destination = "/root/src/"
    source      = "src/"
  }

  provisioner "shell" {
    inline = ["yum install -y git awscli gnupg jq xmlstarlet", "cd /root", "mvn install -f pom.xml", "mvn dependency:go-offline -f deps-pom.xml", "mkdir -p src/main/java", "mvn clean verify -f deps-pom.xml", "rm -rf target", "rm -rf src", "rm -f *.xml", "mv -f .m2/repository local_repo", "mkdir /maven", "rm -rf /etc/localtime", "ln -s /usr/share/zoneinfo/Australia/Sydney /etc/localtime"]
  }

  provisioner "file" {
    destination = "/root/.m2/settings.xml"
    source      = "maven-settings.xml"
  }

  provisioner "file" {
    destination = "/root/.aws/"
    source      = "./aws/"
  }

  post-processors {
    post-processor "docker-tag" {
      name       = "docker.tag"
      repository = "zepben/pipeline-java"
      tags       = ["latest"]
    }
    post-processor "docker-push" {
      name           = "docker.push"
      login          = true
      login_password = "${var.dockerhub_pw}"
      login_username = "${var.dockerhub_user}"
    }
  }
}
