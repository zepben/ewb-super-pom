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

variable "base_image" {
  type = string
  default = "zepben/pipeline-java"
}

source "docker" "image" {
  commit = "true"
  image  = var.base_image
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
    inline = ["cd /root", "mvn install -f pom.xml", "mvn dependency:go-offline -f deps-pom.xml", "mkdir -p src/main/java", "mvn clean verify -f deps-pom.xml", "rm -rf target", "rm -rf src", "rm -f *.xml", "mv -f /maven /root/local_repo", "mkdir /maven", "rm -rf /etc/localtime", "ln -s /usr/share/zoneinfo/Australia/Sydney /etc/localtime"]
  }

  provisioner "file" {
    destination = "/usr/share/maven/conf/settings.xml"
    source      = "maven-settings.xml"
  }

  provisioner "file" {
    destination = "/root/.aws/"
    source      = "./aws/"
  }

  post-processors {
    post-processor "docker-tag" {
      name       = "docker.tag"
      repository = "zepben/pipeline-java-ewb"
      tags       = ["latest", "1.0.0"]
    }
    post-processor "docker-push" {
      name           = "docker.push"
      login          = true
      login_password = "${var.dockerhub_pw}"
      login_username = "${var.dockerhub_user}"
    }
  }
}
