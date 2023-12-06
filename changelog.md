## [0.34.1]

### Breaking Changes
* None.

### New Features
* None.

### Enhancements
* Updated version of gRPC dependencies to `1.59.1`.
* Updated version of GraphQL-Kotlin dependencies to `6.5.6`. From version `7.0.0` onwards, [GraphQL-Kotlin is only
  supported on Java 17+](https://github.com/ExpediaGroup/graphql-kotlin/releases/tag/7.0.0).

### Fixes
* Updated `slf4j-api` to `2.0.9`, which is compatible with the new logback version (`1.4.11`)

### Notes
* None.

## [0.34.0]

### Breaking Changes
* The following dependencies have been moved to a different group ID:
  * `unirest-java` moved from `com.mashape.unirest` to `com.konghq`
  * `dom4j` moved from `dom4j` to `org.dom4j`

### New Features
* None.

### Enhancements
* None.

### Fixes
* Updated vulnerable dependencies to their latest version:
  * Vert.x packages (`3.9.6` to `4.4.6`)
  * GraphQL packages (`19.2` to `21.3`)
  * Ktor packages (`2.1.0` to `2.3.5`)
  * `logback-classic` (`1.2.1` to `1.4.11`)
  * `kotlin-wiremock` (`1.0.1` to `2.0.2`)
  * `guava` (`24.1-jre` to `32.1.3-jre`)
  * `commons-io` (`2.5` to `2.15.0`)
  * `commons-collections4` (`4.2` to `4.4`)
  * `commons-text` (`1.6` to `1.11.0`)
  * `jackson-datatype-jsr310` (`2.6.1` to `2.15.3`)
  * `rest-assured` (`3.2.0` to `5.3.2`)
  * `unirest-java` (`1.4.9` to `3.14.5`)
  * `sqlite-jdbc` (`3.36.0.3` to `3.43.2.2`)
  * `java-jwt` (`3.18.2` to `4.4.0`)
  * `dom4j` (`1.6.1` to `2.1.4`)

### Notes
* None.
