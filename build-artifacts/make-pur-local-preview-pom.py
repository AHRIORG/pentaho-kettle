"""Generate a PUR core POM for the local 10.1 preview build.

The upstream POM stays untouched. Run Maven with
``-f plugins/pur/core/pom.local-preview.xml`` or temporarily substitute the
generated POM into the reactor, restoring the upstream file afterward.
"""

from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/pur/core/pom.xml"
OUTPUT = SOURCE.with_name("pom.local-preview.xml")
MAVEN_NS = "http://maven.apache.org/POM/4.0.0"
VERSION = "9.4.0.0-343"

ET.register_namespace("", MAVEN_NS)
tree = ET.parse(SOURCE)
dependencies = tree.getroot().find(f"{{{MAVEN_NS}}}dependencies")
if dependencies is None:
    raise SystemExit("PUR core has no dependencies element")

changed = set()
for dependency in list(dependencies):
    scope = dependency.findtext(f"{{{MAVEN_NS}}}scope")
    if scope == "test":
        # Maven resolves these even when compilation and execution are skipped.
        dependencies.remove(dependency)
        continue

    artifact = dependency.findtext(f"{{{MAVEN_NS}}}artifactId")
    if artifact in ("pentaho-platform-repository", "pentaho-platform-extensions"):
        version = dependency.find(f"{{{MAVEN_NS}}}version")
        if version is None:
            raise SystemExit(f"Missing version for {artifact}")
        version.text = VERSION
        changed.add(artifact)

if changed != {"pentaho-platform-repository", "pentaho-platform-extensions"}:
    raise SystemExit(f"Unexpected Platform dependencies: {changed}")

# Direct mediation selects the actual 9.4 JAR instead of the missing 10.1
# transitive coordinate inherited from the installed kettle-core POM.
encryption = ET.SubElement(dependencies, f"{{{MAVEN_NS}}}dependency")
for tag, value in (
    ("groupId", "org.pentaho"),
    ("artifactId", "pentaho-encryption-support"),
    ("version", VERSION),
    ("scope", "provided"),
):
    ET.SubElement(encryption, f"{{{MAVEN_NS}}}{tag}").text = value

tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
print(OUTPUT)
