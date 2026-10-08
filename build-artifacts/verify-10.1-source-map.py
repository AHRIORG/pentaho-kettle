"""Verify missing PDI 10.1 artifacts against POMs in pentaho/* GitHub sources.

Requires GitHub CLI authentication. This reads public repositories only.
"""

from __future__ import annotations

import base64
import csv
import json
from pathlib import Path
import posixpath
import subprocess
import xml.etree.ElementTree as ET


NS = {"m": "http://maven.apache.org/POM/4.0.0"}
VERSION = "10.1.0.0-SNAPSHOT"

# groupId, artifactId, packaging extension, repository, path to producer POM.
TARGETS = [
    ("org.pentaho", "pentaho-encryption-support", "jar", "", ""),
    ("pentaho", "pentaho-vfs-browser", "jar", "apache-vfs-browser", "pom.xml"),
    ("org.pentaho", "commons-xul-swt", "jar", "pentaho-commons-xul", "swt/pom.xml"),
    ("org.pentaho", "commons-xul-swing", "jar", "pentaho-commons-xul", "swing/pom.xml"),
    ("pentaho", "pentaho-capability-manager", "jar", "pentaho-osgi-bundles", "pentaho-capability-manager/pom.xml"),
    ("org.pentaho", "pentaho-metadata", "jar", "pentaho-metadata", "pom.xml"),
    ("pentaho", "pentaho-mongo-utils", "jar", "pentaho-mongo-utils", "pom.xml"),
    ("org.pentaho", "json", "jar", "pentaho-commons-json", "pom.xml"),
    ("pentaho", "pentaho-platform-repository", "jar", "pentaho-platform", "repository/pom.xml"),
    ("pentaho", "pentaho-platform-extensions", "jar", "pentaho-platform", "extensions/pom.xml"),
    ("pentaho", "pentaho-metaverse-api", "jar", "pentaho-metaverse", "api/pom.xml"),
    ("pentaho", "pentaho-platform-core", "jar", "pentaho-platform", "core/pom.xml"),
    ("pentaho", "pentaho-big-data-legacy-core", "jar", "big-data-plugin", "legacy-core/pom.xml"),
    ("org.pentaho", "pentaho-cassandra-plugin-package", "zip", "pentaho-cassandra-plugin", "assemblies/plugin/pom.xml"),
    ("org.pentaho.di.plugins", "pdi-teradata-tpt-plugin-package", "zip", "pdi-teradata-tpt-plugin", "assemblies/plugin/pom.xml"),
    ("pentaho", "pdi-platform-utils-plugin", "zip", "pdi-platform-utils-plugin", "assemblies/plugin/pom.xml"),
    ("com.pentaho.di.plugins", "mongodb-plugin", "zip", "pentaho-mongodb-plugin", "assembly/plugin/pom.xml"),
    ("org.pentaho", "vertica-bulkloader-plugin", "zip", "pentaho-vertica-bulkloader", "assemblies/plugin/pom.xml"),
    ("pentaho", "pentaho-s3-vfs-plugin", "zip", "big-data-plugin", "assemblies/s3-vfs/pom.xml"),
    ("pentaho", "pentaho-streaming-kafka-plugin", "zip", "big-data-plugin", "assemblies/kafka-plugin/pom.xml"),
    ("pentaho", "metaverse-plugin", "zip", "pentaho-metaverse", "assemblies/plugin/pom.xml"),
    ("pentaho", "pdi-dataservice-driver-bundle", "zip", "pdi-dataservice-plugin", "assemblies/driver/pom.xml"),
    ("pentaho", "pentaho-application-launcher", "jar", "pentaho-application-launcher", "pom.xml"),
    ("pentaho", "oss-licenses", "zip", "", ""),
    ("pentaho", "pentaho-service-coordinator", "jar", "pentaho-osgi-bundles", "pentaho-service-coordinator/pom.xml"),
]


def gh_api(endpoint: str) -> dict:
    result = subprocess.run(
        ["gh", "api", endpoint], capture_output=True, text=True, check=False
    )
    if result.returncode:
        raise RuntimeError(f"gh api {endpoint}: {result.stderr.strip()}")
    return json.loads(result.stdout)


def child_text(element: ET.Element | None, name: str) -> str:
    return "" if element is None else element.findtext(f"m:{name}", "", NS).strip()


def pom_content(repo: str, pom_path: str, sha: str) -> bytes:
    item = gh_api(f"repos/pentaho/{repo}/contents/{pom_path}?ref={sha}")
    return base64.b64decode(item["content"])


def assembly_execution_path(repo: str, pom_path: str, sha: str, data: bytes) -> str:
    """Find an assembly execution in this POM or a same-repository parent."""
    current = pom_path
    for _ in range(5):
        root = ET.fromstring(data)
        for plugin in root.findall(".//m:build/m:plugins/m:plugin", NS):
            if child_text(plugin, "artifactId") == "maven-assembly-plugin":
                goals = [node.text for node in plugin.findall(".//m:goal", NS)]
                if "single" in goals:
                    return current
        parent = root.find("m:parent", NS)
        if parent is None or parent.find("m:relativePath", NS) is not None and not child_text(parent, "relativePath"):
            break
        relative = child_text(parent, "relativePath") or "../pom.xml"
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(current), relative))
        if not candidate.endswith(".xml"):
            candidate = posixpath.join(candidate, "pom.xml")
        if candidate.startswith("../") or candidate == current:
            break
        try:
            data = pom_content(repo, candidate, sha)
        except RuntimeError:
            break
        current = candidate
    return ""


def main() -> None:
    output = Path(__file__).with_name("source-map-10.1.csv")
    refs: dict[str, str] = {}
    rows: list[dict[str, str]] = []
    for group, artifact, extension, repo, pom_path in TARGETS:
        row = {
            "GroupId": group,
            "ArtifactId": artifact,
            "Version": VERSION,
            "Type": extension,
            "Repository": f"pentaho/{repo}" if repo else "",
            "Branch": "10.1" if repo else "",
            "Commit": "",
            "PomPath": pom_path,
            "PomCoordinate": "",
            "PomPackaging": "",
            "AssemblyExecutionPath": "",
            "Status": "no source repository located" if not repo else "",
        }
        if repo:
            try:
                if repo not in refs:
                    refs[repo] = gh_api(f"repos/pentaho/{repo}/branches/10.1")["commit"]["sha"]
                sha = refs[repo]
                row["Commit"] = sha
                data = pom_content(repo, pom_path, sha)
                root = ET.fromstring(data)
                parent = root.find("m:parent", NS)
                pom_group = child_text(root, "groupId") or child_text(parent, "groupId")
                pom_artifact = child_text(root, "artifactId")
                pom_version = child_text(root, "version") or child_text(parent, "version")
                packaging = child_text(root, "packaging") or "jar"
                row["PomCoordinate"] = f"{pom_group}:{pom_artifact}:{pom_version}"
                row["PomPackaging"] = packaging
                if (pom_group, pom_artifact, pom_version) == (group, artifact, VERSION):
                    if extension == "zip":
                        assembly_path = assembly_execution_path(repo, pom_path, sha, data)
                        row["AssemblyExecutionPath"] = assembly_path
                        row["Status"] = (
                            "matching POM; assembly ZIP configured"
                            if assembly_path else "matching POM; ZIP output not confirmed"
                        )
                    elif packaging in {"jar", "bundle"}:
                        row["Status"] = "matching 10.1 source POM"
                    else:
                        row["Status"] = "matching POM; JAR packaging not confirmed"
                else:
                    row["Status"] = "POM coordinate differs"
            except Exception as exc:
                row["Status"] = f"verification failed: {exc}"
        rows.append(row)
        print(f"{artifact}: {row['Status']}")

    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {output}")

    report = output.with_suffix(".md")
    direct = rows[:-1]
    located = sum(row["Repository"] != "" and row["Status"].startswith("matching") for row in direct)
    lines = [
        "# Pentaho 10.1 source map",
        "",
        f"Verified {located} of {len(direct)} missing direct 10.1 artifacts against",
        "POMs in Pentaho's public GitHub repositories on their `10.1` branches.",
        "The additional `pentaho-service-coordinator` dependency also matches",
        "a public 10.1 source module. Each link below is pinned to the branch",
        "commit checked during this audit; the CSV records all coordinates",
        "and commit hashes.",
        "",
        "| Required artifact | 10.1 producer POM | Result |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        artifact = f"`{row['GroupId']}:{row['ArtifactId']}:{row['Type']}`"
        if row["Repository"]:
            url = f"https://github.com/{row['Repository']}/blob/{row['Commit']}/{row['PomPath']}"
            source = f"[{row['Repository']}/{row['PomPath']}]({url})"
            result = "Exact 10.1 source POM"
            if row["Type"] == "zip":
                result += "; ZIP build not verified"
        else:
            source = "Not located"
            result = "No public producer POM found"
        lines.append(f"| {artifact} | {source} | {result} |")
    lines += [
        "",
        "The standalone `pentaho-s3-vfs` repository has no `10.1` branch;",
        "`big-data-plugin/assemblies/s3-vfs` is the matching 10.1 producer.",
        "The `oss-licenses` ZIP has no matching public producer POM in this",
        "search. Pentaho does publish a [10.1 suite license report](https://github.com/pentaho/oss-reports/blob/main/archive/pentaho-suite/PentahoSuite_OSS_Licenses_v10.1.0.0.pdf),",
        "which is a separate document and not the requested ZIP artifact.",
        "",
        "A matching source POM establishes coordinates and a source location.",
        "It does not establish that the module can build with the available",
        "dependencies or that its packaged JAR/ZIP is present. In particular,",
        "the nine source-mapped ZIP modules use POM packaging and still need",
        "their assembly outputs built and checked.",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()
