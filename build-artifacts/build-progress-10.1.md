# PDI 10.1 local distribution progress

Updated 2026-10-07. This is a **local preview**, not a version-pure or
redistributable 10.1 release.

## Output and smoke test

- Client ZIP: `assemblies/client/target/pdi-ce-10.1.0.0-SNAPSHOT.zip`
  (460,004,642 bytes; SHA-256
  `AD1CB0776CE9375AC4069F8504DFF9013939305A63FD632CB3DAE328B3345090`).
- Extracted preview: `D:\data-integration\pdi-10.1-local-preview\data-integration`.
  The existing 9.4 installation at `D:\data-integration` was left in place.
- The ZIP contains 1,329 entries, including 237 files under `lib`, 63 plugin
  directories, Windows and Unix launchers, five platform SWT artifacts,
  samples, and the 10.1 Data Service JDBC driver bundle.
- With Java 11, `Pan.bat` reported `10.1.0.0-SNAPSHOT`. The included
  `samples\transformations\Generate Row - basics.ktr` completed with 10 rows
  through `Generate Rows` and `Dummy (do nothing)`, exit code 0.

Use a writable metastore directory for the smoke test. `KETTLE_HOME` alone
does not set `PENTAHO_METASTORE_FOLDER`. Without this setting, the sandboxed
launch timed out while trying to create a lock in the default metastore path.
This command completed without that error:

```powershell
$env:PENTAHO_JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-11.0.32.101-hotspot'
$env:KETTLE_HOME = Join-Path $env:TEMP 'kettle-10.1-smoke-home'
$metaStore = Join-Path $env:KETTLE_HOME '.pentaho'
New-Item -ItemType Directory -Path $metaStore -Force | Out-Null
$env:PENTAHO_DI_JAVA_OPTIONS = "-Xms256m -Xmx1024m -DPENTAHO_METASTORE_FOLDER=$metaStore"
Set-Location 'D:\data-integration\pdi-10.1-local-preview\data-integration'
.\Pan.bat '-file=samples\transformations\Generate Row - basics.ktr' '-level=Basic'
```

## Dependency state

`direct-dependencies-10.1-current.csv` has **297 exact artifacts of 301 direct
compile/runtime coordinates** in the temporary Maven cache. This is a direct
POM audit, not proof that every optional plugin has its entire transitive
runtime classpath or that every 10.1 feature works. The four missing exact
coordinates are:

| Requested artifact | Local preview treatment |
| --- | --- |
| `org.pentaho:pentaho-encryption-support:10.1.0.0-SNAPSHOT` | Used the real `9.4.0.0-343` JAR. Basic encryption tests from the earlier core build passed; full compatibility remains unverified. |
| `pentaho:pentaho-platform-repository:10.1.0.0-SNAPSHOT` | Used the real `9.4.0.0-343` JAR in `pdi-libs` and PUR/Metaverse builds. 10.1 source exists, but its build has further unavailable legacy dependencies. |
| `pentaho:pentaho-platform-extensions:10.1.0.0-SNAPSHOT` | Used the real `9.4.0.0-343` JAR in `pdi-libs`, PUR, and Platform Utils. 10.1 source exists, but its build has further unavailable legacy dependencies. |
| `pentaho:oss-licenses:zip:10.1.0.0-SNAPSHOT` | Omitted only for the local preview. The ZIP lacks `PentahoDataIntegration_OSS_Licenses.html`; correct 10.1 notices are required before redistribution. |

The 9.4 artifacts keep their real filenames and Maven versions in the preview:

| Artifact | SHA-256 |
| --- | --- |
| `pentaho-encryption-support-9.4.0.0-343.jar` | `1DC9EB826C51B07572B84EE7160565E91A3357CE7DBE97561577E2E16D2B622E` |
| `pentaho-platform-repository-9.4.0.0-343.jar` | `E63035CEE104DAC69C2FE770F2263B577364E430EE7CC99A65CE46FB8E224A30` |
| `pentaho-platform-extensions-9.4.0.0-343.jar` | `00157CA1524307095369DA02267C859C73A77ABA148BB0F342BBAB4947B90DC2` |

## Source builds and local build adjustments

The core/engine/UI and 10.1 reactor plugin packages were built from this
checkout. Most external producer commits are recorded in
`source-map-10.1.csv`; the Hadoop shim API source was additionally pinned to
`pentaho/pentaho-hadoop-shims@3607e0b6a7a6ee95fa021c5b049930a584912aeb`.
This run additionally built the 10.1 Launcher,
Commons XUL Swing/SWT, OSGI Service Coordinator/Capability Manager/i18n,
VFS Browser, Reporting Engine and eleven reporting extensions, Commons JSON,
Metadata, Version Checker, Platform Core, Metaverse API/Core/Web,
Mongo Utils, Big Data Legacy Core, Hadoop shim API/Core, and the Cassandra,
Teradata TPT, Platform Utils, MongoDB, Vertica, S3 VFS, Kafka Streaming,
Metaverse, and Data Service driver packages.

Local source changes in temporary checkouts were confined to dependencies or
build tooling: use of Central's BeanShell coordinates, SWT/JFace selection for
Java 11, explicit 9.4 Platform/Encryption fallback versions, disabling
unavailable Karaf feature generation where the PDI ZIP needs only JARs, and
removal of an unused Jaxen import in Metaverse Core. The Vertica plugin source
was compiled against `com.vertica.jdbc:vertica-jdbc:11.1.0-0` at its real
version because the source POM's `com.vertica:vertica-jdbc-driver:06.00.0000`
could not be retrieved; database compatibility has not been tested. Its JAR
SHA-256 is `14C62A1E96B4DF7EBBC7011D516A9CCF21F4E8DFAD177744815F302FA573A000`.
Legacy third-party JARs missing from Central were imported from the existing
9.4 installation at their exact requested versions, without relabeling.

The repository POM edits make the fallback versions overridable while keeping
10.1 defaults, pin Java 11 compatible SWT, and remove unused Platform
Extensions declarations from two plugins. `make-pur-local-preview-pom.py`
generates the PUR-only compatibility POM; the generated file and upstream
POM were restored/removed after building. To produce the local preview ZIP,
the `oss-licenses` dependency and assembly dependency set were temporarily
removed, then both original files were restored after Maven packaging.
Source builds and the final assembly used Maven 3.9.16 and Java 11; most
external module tests were skipped. `git diff --check` passed.

## Remaining verification

The Pan sample proves basic CLI execution, not Spoon GUI startup, database
connectivity, encrypted credential round trips, repository operations, or
every bundled plugin. Hadoop shim API JARs were built from 10.1 source for
compilation, but the optional Big Data runtime classpath has not been
validated. Resolve the four exact-version gaps, prepare full 10.1 notices,
and run feature-specific checks before calling this a full 10.1 release.
