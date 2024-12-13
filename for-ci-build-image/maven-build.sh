#!/usr/bin/env bash

# Manipulate pom for dependencies
cp deps-pom-template.xml deps-pom.xml
cp ../pom.xml pom.xml
version=$(cat pom.xml | sed 's/xmlns.*=".*"//g' | xmllint --xpath '/project/version/text()' -)
sed -i "s/{{version}}/$version/g" deps-pom.xml
deps=$(cat pom.xml | sed 's/xmlns.*=".*"//g' | xmllint --xpath '/project/dependencyManagement/dependencies/dependency' -)
deps=$(echo $deps | sed 's/\//\\\//g; s/ /\\n/g')
ln=$(cat deps-pom.xml | grep -n "<dependencies>" | cut -d':' -f1)
ln=$((ln + 1))
sed -i "$ln i $deps" deps-pom.xml
# Scripts to copy plugins from pluginManagement
plugins=$(cat pom.xml | sed 's/xmlns.*=".*"//g' | xmllint --xpath '/project/build/pluginManagement/plugins/plugin' -)
plugins=$(echo $plugins | sed 's/\//\\\//g; s/ /\\n/g')
ln=$(cat deps-pom.xml | grep -n "<plugins>" | cut -d':' -f1)
ln=$((ln + 1))
sed -i "$ln i $plugins" deps-pom.xml
xmllint -format deps-pom.xml > deps-pom-new.xml
mv -f deps-pom-new.xml deps-pom.xml


# Maven download dependencies
mvn install -f pom.xml
mvn dependency:go-offline -f deps-pom.xml
mkdir -p src/main/java
mvn clean verify -f deps-pom.xml
