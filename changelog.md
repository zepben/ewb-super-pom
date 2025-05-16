## [0.39.0]

### Enhancements
- Migrate OSSRH repository to Maven Central

## [0.38.0]

### Enhancements
- Updated to protobuf `4.30.2` and gRPC `1.71.0`
- Removed protobuf compilation plugin - now handled in ewb-grpc repo only

## [0.37.0]

### Enhancements
- Update `azure-bom` property to `1.2.30` to fix workload identity authentication loop
- Update `vertx` to `4.5.11` to fix compatiblity issue with `azure-bom` transitive `netty` dependency

## [0.36.6]

### Enhancements
- Change from using `s3` SDK dependency directly to use AWS SDK BOM

## [0.36.5]

### New Features
* Added `s3` to `dependencyManagement`.

## [0.36.4]

### Fixes
* Fix to run dokka as part of the package process as deploy doesn't seem to run pre-site.

## [0.36.3]

### Fixes
* Generate docs pre-site and specify extra necessary goals for javadocs and sources jars

## [0.36.2]

### Fixes
* Upgrade dokka as 1.4.10 has gone missing from central repos

## [0.36.1]

### Fixes
* Fix gpg login from new issue that only arose on debian

## [0.36.0]

### Breaking Changes
* None.

### New Features
* Added `org.testcontainers.postgresql` to `dependencyManagement`

### Enhancements
* None

### Fixes
* None.

### Notes
* None.

## [0.35.2]

### Breaking Changes
* None.

### New Features
* None.

### Enhancements
* Downgrade version of Ktor to `2.1.0` to solve issue with Netty and HTTP2, see [KTOR-1516](https://youtrack.jetbrains.com/issue/KTOR-6151/Request-hangs-on-Firefox-with-Netty-HTTPS-and-Compression)

### Fixes
* None.

### Notes
* None.

## [0.35.1]

### Breaking Changes
* None.

### New Features
* None.

### Enhancements
* Updated version of Ktor to `2.3.8`.

### Fixes
* None.

### Notes
* None.

## [0.35.0]

### Breaking Changes
* None.

### New Features
* Added `lucene-analysis-common` to `dependencyManagement`.

### Enhancements
* Updated version of Apache Lucene to `9.9.2`.

### Fixes
* None.

### Notes
* None.


## [0.34.1]

### Breaking Changes
* None.

### New Features
* None.

### Enhancements
* Updated version of gRPC dependencies to `1.59.1`.
* Updated version of GraphQL-Kotlin dependencies to `6.5.6`. From version `7.0.0` onwards, [GraphQL-Kotlin is only
  supported on Java 17+](https://github.com/ExpediaGroup/graphql-kotlin/releases/tag/7.0.0).
* Updated `sqlite-jdbc` to `3.44.1.0`, fixing an issue with running certain tests on Windows involving
  round trips for floating-point values.

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
