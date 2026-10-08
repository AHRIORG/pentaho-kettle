# Pentaho 10.1 source map

**Build update:** The source-mapped ZIPs and most JARs have now been built for
a local preview. The per-row results below record source discovery at the
time of the audit; see [build-progress-10.1.md](build-progress-10.1.md) for
the current build result and compatibility fallbacks.

Verified 22 of 24 missing direct 10.1 artifacts against
POMs in Pentaho's public GitHub repositories on their `10.1` branches.
The additional `pentaho-service-coordinator` dependency also matches
a public 10.1 source module. Each link below is pinned to the branch
commit checked during this audit; the CSV records all coordinates
and commit hashes.

| Required artifact | 10.1 producer POM | Result |
| --- | --- | --- |
| `org.pentaho:pentaho-encryption-support:jar` | Not located | No public producer POM found |
| `pentaho:pentaho-vfs-browser:jar` | [pentaho/apache-vfs-browser/pom.xml](https://github.com/pentaho/apache-vfs-browser/blob/48a42bd4b22e7a672f0ac647bddb84481ad896c0/pom.xml) | Exact 10.1 source POM |
| `org.pentaho:commons-xul-swt:jar` | [pentaho/pentaho-commons-xul/swt/pom.xml](https://github.com/pentaho/pentaho-commons-xul/blob/a1590614678791dbd7fbafe5f4adcbf2fdc466f3/swt/pom.xml) | Exact 10.1 source POM |
| `org.pentaho:commons-xul-swing:jar` | [pentaho/pentaho-commons-xul/swing/pom.xml](https://github.com/pentaho/pentaho-commons-xul/blob/a1590614678791dbd7fbafe5f4adcbf2fdc466f3/swing/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-capability-manager:jar` | [pentaho/pentaho-osgi-bundles/pentaho-capability-manager/pom.xml](https://github.com/pentaho/pentaho-osgi-bundles/blob/2459e67d5570eb1ee056bec5dd66130fab7bd4b1/pentaho-capability-manager/pom.xml) | Exact 10.1 source POM |
| `org.pentaho:pentaho-metadata:jar` | [pentaho/pentaho-metadata/pom.xml](https://github.com/pentaho/pentaho-metadata/blob/2f0cd1998f5f19b35183a185abb051baf0b8a87c/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-mongo-utils:jar` | [pentaho/pentaho-mongo-utils/pom.xml](https://github.com/pentaho/pentaho-mongo-utils/blob/d61ff8b8d30f02c6b425cab85a67368947767600/pom.xml) | Exact 10.1 source POM |
| `org.pentaho:json:jar` | [pentaho/pentaho-commons-json/pom.xml](https://github.com/pentaho/pentaho-commons-json/blob/0d6f90380a20b39a8276ad37c27bee08552bd97e/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-platform-repository:jar` | [pentaho/pentaho-platform/repository/pom.xml](https://github.com/pentaho/pentaho-platform/blob/4161c8117ff3a01b5a64be66f9869bed36f1a0f0/repository/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-platform-extensions:jar` | [pentaho/pentaho-platform/extensions/pom.xml](https://github.com/pentaho/pentaho-platform/blob/4161c8117ff3a01b5a64be66f9869bed36f1a0f0/extensions/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-metaverse-api:jar` | [pentaho/pentaho-metaverse/api/pom.xml](https://github.com/pentaho/pentaho-metaverse/blob/77c22b424d1d6fda5c29b1e9a81f57bd20abe36f/api/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-platform-core:jar` | [pentaho/pentaho-platform/core/pom.xml](https://github.com/pentaho/pentaho-platform/blob/4161c8117ff3a01b5a64be66f9869bed36f1a0f0/core/pom.xml) | Exact 10.1 source POM |
| `pentaho:pentaho-big-data-legacy-core:jar` | [pentaho/big-data-plugin/legacy-core/pom.xml](https://github.com/pentaho/big-data-plugin/blob/87c0023236c0530ce93b47381c36288863bd5443/legacy-core/pom.xml) | Exact 10.1 source POM |
| `org.pentaho:pentaho-cassandra-plugin-package:zip` | [pentaho/pentaho-cassandra-plugin/assemblies/plugin/pom.xml](https://github.com/pentaho/pentaho-cassandra-plugin/blob/943f05753537af7ea19c5e8fec956f56e4ba71f5/assemblies/plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `org.pentaho.di.plugins:pdi-teradata-tpt-plugin-package:zip` | [pentaho/pdi-teradata-tpt-plugin/assemblies/plugin/pom.xml](https://github.com/pentaho/pdi-teradata-tpt-plugin/blob/716260d3ee852c69bb7b48cbf85d37060cfeb14f/assemblies/plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `pentaho:pdi-platform-utils-plugin:zip` | [pentaho/pdi-platform-utils-plugin/assemblies/plugin/pom.xml](https://github.com/pentaho/pdi-platform-utils-plugin/blob/8663da2b0db367c5006cdc5b4ea10d068949d68f/assemblies/plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `com.pentaho.di.plugins:mongodb-plugin:zip` | [pentaho/pentaho-mongodb-plugin/assembly/plugin/pom.xml](https://github.com/pentaho/pentaho-mongodb-plugin/blob/45cb03b9da170568996f726457862d1a1e04c9a0/assembly/plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `org.pentaho:vertica-bulkloader-plugin:zip` | [pentaho/pentaho-vertica-bulkloader/assemblies/plugin/pom.xml](https://github.com/pentaho/pentaho-vertica-bulkloader/blob/9ff59df46feba7fde184928972bcd5a43fb0a90e/assemblies/plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `pentaho:pentaho-s3-vfs-plugin:zip` | [pentaho/big-data-plugin/assemblies/s3-vfs/pom.xml](https://github.com/pentaho/big-data-plugin/blob/87c0023236c0530ce93b47381c36288863bd5443/assemblies/s3-vfs/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `pentaho:pentaho-streaming-kafka-plugin:zip` | [pentaho/big-data-plugin/assemblies/kafka-plugin/pom.xml](https://github.com/pentaho/big-data-plugin/blob/87c0023236c0530ce93b47381c36288863bd5443/assemblies/kafka-plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `pentaho:metaverse-plugin:zip` | [pentaho/pentaho-metaverse/assemblies/plugin/pom.xml](https://github.com/pentaho/pentaho-metaverse/blob/77c22b424d1d6fda5c29b1e9a81f57bd20abe36f/assemblies/plugin/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `pentaho:pdi-dataservice-driver-bundle:zip` | [pentaho/pdi-dataservice-plugin/assemblies/driver/pom.xml](https://github.com/pentaho/pdi-dataservice-plugin/blob/465c82b17492a8ea11f2f0a2cf1f70f98e67a7be/assemblies/driver/pom.xml) | Exact 10.1 source POM; ZIP build not verified |
| `pentaho:pentaho-application-launcher:jar` | [pentaho/pentaho-application-launcher/pom.xml](https://github.com/pentaho/pentaho-application-launcher/blob/81a7b0a14c3499842167ab4d1a56f3690996bdf5/pom.xml) | Exact 10.1 source POM |
| `pentaho:oss-licenses:zip` | Not located | No public producer POM found |
| `pentaho:pentaho-service-coordinator:jar` | [pentaho/pentaho-osgi-bundles/pentaho-service-coordinator/pom.xml](https://github.com/pentaho/pentaho-osgi-bundles/blob/2459e67d5570eb1ee056bec5dd66130fab7bd4b1/pentaho-service-coordinator/pom.xml) | Exact 10.1 source POM |

The standalone `pentaho-s3-vfs` repository has no `10.1` branch;
`big-data-plugin/assemblies/s3-vfs` is the matching 10.1 producer.
The `oss-licenses` ZIP has no matching public producer POM in this
search. Pentaho does publish a [10.1 suite license report](https://github.com/pentaho/oss-reports/blob/main/archive/pentaho-suite/PentahoSuite_OSS_Licenses_v10.1.0.0.pdf),
which is a separate document and not the requested ZIP artifact.

A matching source POM establishes coordinates and a source location.
It does not establish that the module can build with the available
dependencies or that its packaged JAR/ZIP is present. In particular,
the nine source-mapped ZIP modules use POM packaging and still need
their assembly outputs built and checked.
