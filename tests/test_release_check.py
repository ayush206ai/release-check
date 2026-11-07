from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "release_check.py"


class ReleaseCheckTests(unittest.TestCase):
    def run_check(self, tag, changelog, metadata='[project]\nversion = "1.2.0"\n'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text(metadata, encoding="utf-8")
            (root / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), tag],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_matching_release(self):
        result = self.run_check("v1.2.0", "## [1.2.0] - 2026-11-07\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tag_mismatch(self):
        result = self.run_check("v1.1.0", "## 1.1.0\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not match", result.stderr)

    def test_missing_heading(self):
        result = self.run_check("1.2.0", "## 1.2.0rc1\n~~~\n## 1.2.0\n~~~\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("No changelog heading", result.stderr)

    def test_dynamic_version(self):
        result = self.run_check("v1.2.0", "## 1.2.0\n", '[project]\ndynamic = ["version"]')
        self.assertEqual(result.returncode, 2)
        self.assertIn("static", result.stderr)

    def test_invalid_toml(self):
        result = self.run_check("v1.2.0", "## 1.2.0\n", "[project")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cannot read release files", result.stderr)
