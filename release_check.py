"""Check a Python package's release tag and changelog."""

import argparse
from pathlib import Path
import re
import tomllib


def has_release_heading(changelog, version):
    escaped = re.escape(version)
    pattern = rf"^ {{0,3}}#{{1,6}}[ \t]+(?:\[v?{escaped}\]|v?{escaped})(?=[ \t#]|$)"
    fence = None
    for line in changelog.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        elif re.match(pattern, line):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="release tag, such as v1.2.0")
    parser.add_argument("--project", type=Path, default=Path("pyproject.toml"))
    parser.add_argument("--changelog", type=Path, default=Path("CHANGELOG.md"))
    args = parser.parse_args()

    try:
        with args.project.open("rb") as source:
            metadata = tomllib.load(source)
        changelog = args.changelog.read_text(encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read release files: {error}\n")

    project = metadata.get("project")
    version = project.get("version") if isinstance(project, dict) else None
    if not isinstance(version, str) or not version.strip():
        parser.exit(2, "Set a static [project].version in pyproject.toml.\n")

    tag_version = args.tag.removeprefix("v")
    problems = []
    if tag_version != version:
        problems.append(f"Tag {args.tag} does not match package version {version}.")
    if not has_release_heading(changelog, tag_version):
        problems.append(f"No changelog heading for release {tag_version}.")
    if problems:
        parser.exit(1, "\n".join(problems) + "\n")

    print(f"Release {args.tag} passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
