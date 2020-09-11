The files in this directory is for creating a Docker image used for building java projects. The image will contain a local repo of dependencies as specified in [pom.xml](../pom.xml).

### Creating the image
[Packer](https://www.packer.io/) is used for building the docker image.

`packer build build-container.json`
`packer build release-container.json`

### build-container.json
This is a config that will build a Docker image with pre downloaded dependencies.

### release-container.json
This is a config that will build a Docker image based from the image produced in build-container.json and install git and xmlstarlet.

### src
The [maven dependency plugin](https://maven.apache.org/plugins/maven-dependency-plugin/) does not do a good job of downloading the entire dependency tree of a plugin. Some plugin dependency won't be downloaded until the time it is used. As a workaround, the files here are just stubs to force the maven compile and surefire plugins to run.

### deps-pom-template.xml
This is a template pom file that will be injected with the dependencies and plugins from [pom.xml](../pom.xml). See 
[bitbucket-pipelines.yml](../bitbucket-pipelines.yml) -> `build docker image for ci` for the script.

### maven-settings.xml
This is the maven settings that will be used when building a Java project.