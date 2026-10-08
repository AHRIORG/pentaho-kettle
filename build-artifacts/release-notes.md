Local source build of Kettle 10.1, prepared as a draft for review.

Assets:
- `kettle-10.1-local.zip`: 15 source-built JARs, SHA-256 checksums, source revisions, local binary input manifest, license files available in source repositories, and test logs.
- `kettle-core-10.1.0.0-SNAPSHOT.jar` and `kettle-engine-10.1.0.0-SNAPSHOT.jar`: the two main JARs for direct inspection.

Verification: Kettle core 1,243 tests passed (one skipped); Kettle engine 2,332 passed (four skipped); Pentaho Platform API 114 passed. The engine test JVM used `-noverify` for legacy PowerMock, and the Windows test environment used a same-drive temporary directory and LF line endings for one fixture. These switches were not applied to the production JARs.

The build used 23 exact-coordinate JARs already present in a local Pentaho Data Integration 9.4 installation. Two were older Pentaho support libraries: `pentaho-encryption-support-9.4.0.0-343` and `pentaho-service-coordinator-9.4.0.0-343`. No binary was relabelled as 10.1. The exact input versions and hashes are in `BINARY_INPUTS.csv` inside the ZIP.

This is not a complete runnable Kettle distribution. The normal license helper was unavailable and disabled for the local build; dependency license and notice packaging and broader runtime checks remain before publication or production use.
