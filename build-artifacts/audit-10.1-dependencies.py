"""Inventory direct Maven dependencies needed by the PDI 10.1 client assembly.

This is a static audit of the checked-out POMs. Maven still has to resolve
transitive dependencies and build the reactor before a distribution is complete.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re
import xml.etree.ElementTree as ET


NS = {"m": "http://maven.apache.org/POM/4.0.0"}
MODULES = (
    "core",
    "engine",
    "ui",
    "assemblies/static",
    "assemblies/lib",
    "assemblies/plugins",
    "assemblies/client",
)
PROPERTY = re.compile(r"\$\{([^}]+)\}")


def value(node: ET.Element | None, path: str) -> str:
    if node is None:
        return ""
    return node.findtext(path, default="", namespaces=NS).strip()


def pom_info(path: Path) -> tuple[ET.Element, dict[str, str], str, str, str]:
    root = ET.parse(path).getroot()
    parent = root.find("m:parent", NS)
    group = value(root, "m:groupId") or value(parent, "m:groupId")
    artifact = value(root, "m:artifactId")
    version = value(root, "m:version") or value(parent, "m:version")
    props = {
        child.tag.rsplit("}", 1)[-1]: (child.text or "").strip()
        for child in root.findall("m:properties/*", NS)
    }
    return root, props, group, artifact, version


def interpolate(text: str, props: dict[str, str]) -> str:
    for _ in range(8):
        new = PROPERTY.sub(lambda m: props.get(m.group(1), m.group(0)), text)
        if new == text:
            break
        text = new
    return text


def inherited_model(
    path: Path,
    source_poms: dict[tuple[str, str, str], Path],
    cache: Path,
    seen: set[Path] | None = None,
) -> tuple[dict[str, str], dict[tuple[str, str, str, str], str]]:
    """Collect properties and managed versions from the local parent chain."""
    seen = set() if seen is None else seen
    if path in seen or not path.is_file():
        return {}, {}
    seen.add(path)
    root, local_props, _, _, project_version = pom_info(path)
    props: dict[str, str] = {}
    managed: dict[tuple[str, str, str, str], str] = {}
    parent = root.find("m:parent", NS)
    if parent is not None:
        parent_key = (
            value(parent, "m:groupId"),
            value(parent, "m:artifactId"),
            value(parent, "m:version"),
        )
        parent_path = source_poms.get(parent_key)
        if parent_path is None:
            group, artifact, version = parent_key
            parent_path = cache / Path(*group.split(".")) / artifact / version / f"{artifact}-{version}.pom"
        props, managed = inherited_model(parent_path, source_poms, cache, seen)
    props = {**props, **local_props, "project.version": project_version, "pom.version": project_version}
    for dep in root.findall("m:dependencyManagement/m:dependencies/m:dependency", NS):
        key = (
            interpolate(value(dep, "m:groupId"), props),
            interpolate(value(dep, "m:artifactId"), props),
            value(dep, "m:type") or "jar",
            value(dep, "m:classifier"),
        )
        version = interpolate(value(dep, "m:version"), props)
        if version:
            managed[key] = version
    return props, managed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache", type=Path, required=True, help="Maven local repository")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    pom_paths = list(args.repo.rglob("pom.xml"))
    source_poms: dict[tuple[str, str, str], Path] = {}
    for path in pom_paths:
        if "target" in path.relative_to(args.repo).parts:
            continue
        _, _, group, artifact, version = pom_info(path)
        source_poms[(group, artifact, version)] = path
    producers = set(source_poms)

    rows: list[dict[str, str]] = []
    for module in MODULES:
        pom_path = args.repo / module / "pom.xml"
        root, _, _, _, _ = pom_info(pom_path)
        props, managed = inherited_model(pom_path, source_poms, args.cache)
        for dep in root.findall("m:dependencies/m:dependency", NS):
            group = interpolate(value(dep, "m:groupId"), props)
            artifact = interpolate(value(dep, "m:artifactId"), props)
            version = interpolate(value(dep, "m:version"), props)
            extension = value(dep, "m:type") or "jar"
            classifier = value(dep, "m:classifier")
            scope = value(dep, "m:scope") or "compile"
            if not version:
                version = managed.get((group, artifact, extension, classifier), "")
            if scope in {"test", "provided"}:
                continue
            filename = f"{artifact}-{version}"
            if classifier:
                filename += f"-{classifier}"
            filename += f".{extension}"
            artifact_path = args.cache / Path(*group.split(".")) / artifact / version / filename
            in_reactor = (group, artifact, version) in producers
            if not version or "${" in version:
                status = "version unresolved in module POM"
            elif artifact_path.is_file():
                status = "cached exact artifact"
            elif in_reactor:
                status = "source in reactor; artifact not built"
            else:
                status = "missing external artifact"
            rows.append({
                "Module": module,
                "GroupId": group,
                "ArtifactId": artifact,
                "Version": version,
                "Type": extension,
                "Classifier": classifier,
                "Scope": scope,
                "Status": status,
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    from collections import Counter

    print(f"Wrote {len(rows)} direct dependencies to {args.output}")
    for status, count in sorted(Counter(row["Status"] for row in rows).items()):
        print(f"{status}: {count}")


if __name__ == "__main__":
    main()
