# Kettle 10.1 local JAR build

This folder contains 15 JARs compiled on Windows with Temurin JDK 11 and Maven 3.9.16. The main outputs are `jars/kettle-core-10.1.0.0-SNAPSHOT.jar` and `jars/kettle-engine-10.1.0.0-SNAPSHOT.jar`. The other JARs are source-built dependencies and APIs. The files are **not a complete, runnable Kettle distribution**; other runtime libraries and plugins are still needed.

## Source revisions

| Source repository | Revision |
| --- | --- |
| [AHRIORG/pentaho-kettle](https://github.com/AHRIORG/pentaho-kettle/tree/10.1) | `2f23e4e513de7893a2b57d688adbaed190cb3b9c` |
| [AHRIORG/maven-parent-poms](https://github.com/AHRIORG/maven-parent-poms/tree/10.1) | `3614095804ac338a70d53bcca99105d4239946a4` |
| [AHRIORG/metastore](https://github.com/AHRIORG/metastore/tree/10.1) | `4a32d717b34c51822725a788d6c9c021b980887d` |
| [AHRIORG/pentaho-registry](https://github.com/AHRIORG/pentaho-registry/tree/10.1) | `99e2e5f20c0dff799ba5ab01d1906b6b016d39ce` |
| [AHRIORG/pentaho-reporting](https://github.com/AHRIORG/pentaho-reporting/tree/10.1) | `ac9b5bf04e0093669c67780e53529470f470ebfa` |
| [AHRIORG/pentaho-connections](https://github.com/AHRIORG/pentaho-connections/tree/10.1) | `723263e5291b50c475b2d828cd526412242eff6c` |
| [AHRIORG/pentaho-actionsequence-dom](https://github.com/AHRIORG/pentaho-actionsequence-dom/tree/10.1) | `cc1ffc7dc804275355103269d9472b91da446573` |
| [AHRIORG/pentaho-commons-xul](https://github.com/AHRIORG/pentaho-commons-xul/tree/10.1) | `a1590614678791dbd7fbafe5f4adcbf2fdc466f3` |
| [AHRIORG/pentaho-commons-database](https://github.com/AHRIORG/pentaho-commons-database/tree/10.1) | `21712945c3258eb8f0f6a54ff517d32f6bebeb18` |
| [AHRIORG/pentaho-platform](https://github.com/AHRIORG/pentaho-platform/tree/10.1) | `4161c8117ff3a01b5a64be66f9869bed36f1a0f0` |
| [AHRIORG/mondrian](https://github.com/AHRIORG/mondrian/tree/10.1) | `4ca46123f10ebb97a3faf9e50fc15dcc18468eb8` |
| [AHRIORG/pentaho-simple-jndi](https://github.com/AHRIORG/pentaho-simple-jndi/tree/simple-jndi-1.0.13) | `fb810b8ebdb739af7b4a9132059d15605a9b7ac5` (tag `simple-jndi-1.0.13`) |

## Local binary inputs

The 10.1 build could not retrieve some dependencies from Pentaho's Maven server. I imported 23 JARs already present in `D:\data-integration` into a temporary Maven cache, with their **actual** Maven coordinates and versions. The full list, original paths, and SHA-256 hashes are in `BINARY_INPUTS.csv`.

Two of those inputs are particularly important: `pentaho-encryption-support-9.4.0.0-343.jar` and `pentaho-service-coordinator-9.4.0.0-343.jar`. Their source was not located, so the 10.1 core and platform API compile against these 9.4 binaries. No JAR was relabelled as a 10.1 version. The older JUG dependency was available locally at its exact requested version, `2.0.0`.

Only temporary build copies were adjusted: the local parent POM's unavailable license helper execution was disabled; Simple JNDI's 9.5 parent was replaced with the available 10.1 parent; Mondrian's absent, test-only `olap4j-tck` dependency was omitted; and local Maven descriptors recorded the 9.4 input versions. The public `build-helper-maven-plugin` 3.3.0 replaced the unavailable Pentaho variant. No source POM change was committed to the forks.

## Verification and limitations

`SHA256SUMS.txt` verifies the 15 compiled JARs. The 10.1 core suite passed 1,243 tests (one skipped), and the 10.1 engine suite passed 2,332 tests (four skipped), with zero failures or errors. The platform API passed 114 tests. The other source-built modules also passed their local test suites: Metastore 120, Registry 20, LibBase 33, LibFormula 185, Connections 60, Action Sequence DOM 1, Commons XUL Core 32, Commons Database Model 300, Simple JNDI 3, and PDI Engine API 12. Mondrian's tests were unavailable because its test-only `olap4j-tck` dependency was absent.

The engine test run used `-noverify` **only in the test JVM** for the legacy PowerMock framework. It also used a same-drive temporary folder and the repository's LF line endings for one CSV fixture; the normal Windows checkout converted that fixture to CRLF. No production JAR was built with `-noverify`. Copies of available source repository license files are in `licenses/`; they do not replace a full dependency license review.

This source-built JAR bundle is retained for build provenance. It needs a complete runtime dependency set, license and notice packaging, and broader compatibility checks before production use or redistribution. The disabled license helper means this folder does not contain its usual generated license bundle.
