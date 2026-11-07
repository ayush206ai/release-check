# Release Check

Catch a version mismatch or missing changelog entry before publishing a Python package.

## Run it

Requires Python 3.11 or newer. Copy `release_check.py` into your repository and run it from the repository root.

```sh
python release_check.py v1.2.0
```

The tag may have a lowercase `v` prefix. After stripping it, the tool compares the tag exactly against the static `[project].version` in `pyproject.toml`. Add a Markdown heading for the tagged release, such as `## [1.2.0] - 2026-11-07` or `## 1.2.0`.

Use `--project` or `--changelog` if your files live elsewhere. Exit codes are 0 for a pass, 1 for a failed check, and 2 for invalid input or unreadable files. This version supports static package versions and Markdown headings that start with the version.

## GitHub Actions

Copy `examples/release-check.yml` into `.github/workflows/` in your package repo. If you already have a publishing workflow, add the check as a step before the publish step so a failed check blocks publication.

## Run the tests

```sh
python -m unittest discover -s tests -v
```
