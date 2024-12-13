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

variable "tags" {
  type = list(string)
  default = ["latest"]
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
    script = "maven-build.sh"
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
      tags       = var.tags
    }
    post-processor "docker-push" {
      name           = "docker.push"
      login          = true
      login_password = "${var.dockerhub_pw}"
      login_username = "${var.dockerhub_user}"
    }
  }
}
