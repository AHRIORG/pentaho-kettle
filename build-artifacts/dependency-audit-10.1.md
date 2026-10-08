# PDI 10.1 distribution dependency audit

**Progress update, 2026-10-07:** A local PDI client preview ZIP has since
been assembled and a sample transformation completed. The latest direct audit
is `direct-dependencies-10.1-current.csv`: 297 of 301 exact coordinates are
cached. Four exact 10.1 inputs still need resolution or replacement before a
version-pure release. See [build-progress-10.1.md](build-progress-10.1.md)
for the ZIP, smoke test, fallback versions, and remaining limits. The counts
and blockers below describe the initial audit before these builds.

Audited on 2026-10-07 against `pentaho-kettle` commit
`2f23e4e513de7893a2b57d688adbaed190cb3b9c` and the temporary Maven
cache used for the existing source-built JAR bundle.

## Result

The existing `kettle-10.1-local.zip` contains 15 verified source-built JARs.
It is **not** a complete or runnable PDI distribution. The full desktop
client is assembled by `assemblies/client/pom.xml` into `pdi-ce` and requires
library, plugin, static-asset, sample, launcher, driver, and license artifacts.
The `pdi-ce` reactor contains 280 modules.

`direct-dependencies-10.1.csv` inventories the direct compile/runtime
dependencies declared by `core`, `engine`, `ui`, and the client, library,
plugin, and static assembly POMs. It records **301** entries:

| State | Count |
| --- | ---: |
| Exact artifact in the temporary Maven cache | 161 |
| Source project in this reactor, artifact not built | 64 |
| External artifact absent from the temporary Maven cache | 76 |

Of the 76 missing external artifacts, **24 request
`10.1.0.0-SNAPSHOT`**. They include `pentaho-encryption-support`,
`pentaho-vfs-browser`, `pentaho-capability-manager`, `pentaho-metadata`,
`pentaho-metaverse-api`, the platform core/repository/extensions JARs,
eight external plugin ZIPs, the data-service driver bundle, the application
launcher, and `oss-licenses`. See the CSV for every exact coordinate.
`pentaho-service-coordinator:10.1.0.0-SNAPSHOT` is an additional dependency
of the platform core source project. The source for that library and for
`pentaho-encryption-support` was not available in the checked-out repositories.
The subsequent [public GitHub source search](source-map-10.1.md) matched
22 of the 24 missing direct 10.1 coordinates to source POMs on Pentaho's
`10.1` branches, and also found the service coordinator source. No public
Pentaho source producer was found for `pentaho-encryption-support` or the
`oss-licenses` ZIP. The matching source modules still need to be built.

The POMs also require third-party artifacts not yet in the temporary cache.
Some may be obtainable from Maven Central or the local 9.4 installation at
their **actual** versions. Their availability has not been taken as proof of a
complete 10.1 transitive dependency graph.

## Resolution checks

- An offline `mvn -pl :pdi-ce -am validate` reached module 166/280 after
  temporarily replacing the unavailable Pentaho build-helper variant and
  disabling the unavailable license helper in the temporary parent POM. It
  stopped at the missing `maven-remote-resources-plugin:1.6.0`. This is a
  build-tool cache gap; Maven Central serves the plugin.
- An offline `dependency:tree` for `assemblies/client/pom.xml` identified
  missing `pdi-dataservice-driver-bundle`, `pentaho-application-launcher`,
  `oss-licenses`, five SWT platform JARs, and the four local assembly ZIPs
  that have not yet been built.
- The repository URL configured in the 10.1 POMs,
  `repo.orl.eng.hitachivantara.com`, did not resolve on this machine.
  `https://repo.pentaho.com/artifactory/pnt-mvn/` responded **HTTP 401** for
  the 10.1 data-service driver metadata. The older `repo.pentaho.org`
  endpoint returned an HTML application page for the same Maven metadata URL,
  not Maven XML.

No 9.4 JAR has been renamed or relabelled as a 10.1 artifact. The existing
source-built bundle's two 9.4 support-library inputs remain identified by
their real coordinates in `kettle-10.1-local/BINARY_INPUTS.csv`.

## Options for the two source-unlocated artifacts

| Artifact | Local-build option | Limit |
| --- | --- | --- |
| `org.pentaho:pentaho-encryption-support:10.1.0.0-SNAPSHOT` | Keep the available `9.4.0.0-343` JAR under its **real version**, with an explicit dependency override. | This is a compatibility fallback, not a verified 10.1 dependency. Do not omit it or substitute a no-op stub: core constants, credential decoding, and password encoder plugin loading use its classes. |
| `pentaho:oss-licenses:zip:10.1.0.0-SNAPSHOT` | For a local runtime build, remove this ZIP dependency and its assembly dependency set in the build copy, and identify the missing 10.1 notices in the output. Pentaho's published 10.1 suite license PDF is a reference for preparing complete notices. | The ZIP supplies `PentahoDataIntegration_OSS_Licenses.html` to the client assembly. An empty or 9.4 HTML file must not be represented as a 10.1 license bundle. Review and package the correct notices before redistribution. |

The 9.4 encryption JAR contains the `Encr`, `PasswordEncoderException`,
`KettleTwoWayPasswordEncoder`, and `AESTwoWayPasswordEncoder` classes referenced
by the 10.1 source and plugin descriptor. The existing core build and tests used
this binary as a 9.4 input; `EncrTest` (4 tests) and
`DecryptingDataSourceTest` (1 test) passed. Those tests support basic backward
compatibility but do not establish full 10.1 behavior or compatibility with
all encrypted credentials. A complete client still needs a launch and
credential round-trip check with the chosen binary.

These options address only the two missing public producer POMs. The other
22 source-mapped 10.1 artifacts are not yet built, and the broader audit still
has unresolved third-party and reactor outputs. Neither option turns the
current 15-JAR bundle into a full PDI distribution.

## Required to finish

The 22 source-matched direct artifacts can be attempted from their 10.1
branches. For a version-pure distribution, `pentaho-encryption-support` still
needs its actual 10.1 source or binary, and `oss-licenses` needs the exact ZIP
or complete equivalent license and notice packaging. An official `pdi-ce` 10.1
client ZIP or access to the authenticated Pentaho artifact repository would
also supply these inputs for inspection and verification. Then resolve all
transitive dependencies, build the reactor and client assembly, and verify
the ZIP and runtime launchers. The current files should not be described or
published as a complete PDI distribution.

The audit can be rerun with:

```powershell
python build-artifacts/audit-10.1-dependencies.py `
  --cache C:\path\to\maven-repository `
  --output build-artifacts/direct-dependencies-10.1.csv
```
