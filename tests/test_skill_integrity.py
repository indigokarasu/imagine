"""Integrity tests for the ocas-imagine skill.

Run: python3 -m unittest discover -s tests

These tests guard the skill package itself: frontmatter validity, dead
references, orphaned reference files, merge-conflict markers, and the
integrity of bundled data files. No network access required.
"""
import json
import os
import re
import unittest

try:
    import yaml
except ImportError:  # pragma: no cover - PyYAML is installed in CI
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")
REFS_DIR = os.path.join(SKILL_DIR, "references")

SKILL_NAME_RE = re.compile(r"^ocas-[a-z0-9]+(?:-[a-z0-9]+)*$")
REPO_SLUG_RE = re.compile(r"github\.com/[^/]+/([A-Za-z0-9._\-]+)")

TEXT_SUFFIXES = (".md", ".json", ".jsonl", ".py", ".yml", ".yaml")
SUPPORT_REF_RE = re.compile(r"(?:references|scripts|assets|templates)/[A-Za-z0-9._\-/]+")
REF_FILE_RE = re.compile(r"references/([A-Za-z0-9._\-]+\.md)")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter_block(text):
    assert text.startswith("---"), "SKILL.md must start with a --- fence"
    end = text.index("\n---", 3)
    return text[3:end]


def support_map_section(text):
    start = text.index("## Support File Map")
    rest = text[start:]
    nxt = rest.find("\n## ", 5)
    return rest[:nxt] if nxt != -1 else rest


class TestFrontmatter(unittest.TestCase):
    def test_frontmatter_parses_with_required_fields(self):
        if yaml is None:
            self.skipTest("PyYAML not installed")
        fm = yaml.safe_load(frontmatter_block(read(SKILL_MD)))
        self.assertRegex(fm["name"], SKILL_NAME_RE)
        self.assertTrue(fm.get("description"))
        self.assertLessEqual(len(fm["description"]), 1024)
        self.assertIn("license", fm)
        self.assertIn("hermes", fm.get("metadata", {}))
        self.assertIn("category", fm["metadata"]["hermes"])
        self.assertIn("references/**", fm.get("includes", []))

    def test_license_appears_early_in_file(self):
        # The library's D1 heuristic checks the first 500 chars of SKILL.md.
        self.assertIn("license", read(SKILL_MD)[:500].lower())

    def test_name_matches_declared_source_repo(self):
        """The skill name is 'ocas-' plus the source repo slug.

        This is the real identity link between frontmatter and the repo.
        The checkout directory name is deliberately NOT used: skill repos
        are published under short names ('imagine') while frontmatter keeps
        the 'ocas-' prefix, and a local clone can be named anything.
        """
        if yaml is None:
            self.skipTest("PyYAML not installed")
        fm = yaml.safe_load(frontmatter_block(read(SKILL_MD)))
        source = fm.get("source", "")
        slug = REPO_SLUG_RE.search(source)
        if not slug:
            self.skipTest(f"source is not a GitHub repo URL: {source!r}")
        self.assertEqual(fm["name"], "ocas-" + slug.group(1))


class TestReferences(unittest.TestCase):
    def test_every_referenced_support_file_exists(self):
        text = read(SKILL_MD)
        for ref in sorted(set(SUPPORT_REF_RE.findall(text))):
            self.assertTrue(
                os.path.exists(os.path.join(SKILL_DIR, ref)),
                f"SKILL.md references a missing file: {ref}",
            )

    def test_support_map_covers_every_reference_file(self):
        text = read(SKILL_MD)
        section = support_map_section(text)
        on_disk = {f for f in os.listdir(REFS_DIR) if f.endswith(".md")}
        mapped = set(REF_FILE_RE.findall(section))
        self.assertEqual(
            sorted(on_disk - mapped), [], "reference files missing from the support file map"
        )

    def test_support_map_uses_when_to_read_column(self):
        self.assertIn("when to read", support_map_section(read(SKILL_MD)).lower())

    def test_no_merge_conflict_markers(self):
        markers = (("<" * 7) + " ", "=" * 7, (">" * 7) + " ")
        for root, _dirs, files in os.walk(SKILL_DIR):
            if ".git" in root.split(os.sep):
                continue
            for name in files:
                path = os.path.join(root, name)
                if os.path.abspath(path) == os.path.abspath(__file__):
                    continue  # this file defines the marker patterns
                if name.endswith(TEXT_SUFFIXES):
                    content = read(path)
                    for marker in markers:
                        self.assertNotIn(marker, content, f"conflict marker in {path}")


class TestDataFiles(unittest.TestCase):
    def test_styles_jsonl_records_are_valid(self):
        path = os.path.join(SKILL_DIR, "styles.jsonl")
        for lineno, line in enumerate(read(path).splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            self.assertIn("name", record, f"styles.jsonl line {lineno} missing name")
            self.assertIn("prompt", record, f"styles.jsonl line {lineno} missing prompt")

    def test_evals_files_parse(self):
        for rel in ("evals.json", os.path.join("evals", "evals.json")):
            path = os.path.join(SKILL_DIR, rel)
            if os.path.exists(path):
                json.loads(read(path))


if __name__ == "__main__":
    unittest.main()
