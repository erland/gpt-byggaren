"""Self-hosting canonical Skills regression: no lost or reordered instruction text."""
from pathlib import Path
import importlib.util
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("canonical_skill_sources", ROOT / "scripts/lib/canonical_skill_sources.py")
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)


def test_self_modular_assembly_is_byte_identical_to_legacy_instruction():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    assert cfg["instructions"]["mode"] == "modular_skills"
    definitions = cfg["skills"]["definitions"]
    assert len(definitions) == 3
    assert {s["id"] for s in definitions} == {
        "gpt-project-workflow", "legacy-project-analysis", "distribution-and-parity"
    }
    compiled = compiler.projected_instruction(ROOT, cfg, definitions)
    previous = (ROOT / "src/instructions/system.md").read_text(encoding="utf-8")
    assert compiled == previous


def test_self_skills_have_distinct_behavior_and_shared_core():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    skills = cfg["skills"]["definitions"]
    core = (ROOT / cfg["instructions"]["core"]).read_text(encoding="utf-8").strip()
    for skill in skills:
        body = compiler.skill_instruction(ROOT, cfg, skills, skill)
        own = (ROOT / skill["source"]).read_text(encoding="utf-8").strip()
        assert core in body
        assert own in body
        for other in skills:
            if other["id"] != skill["id"]:
                other_body = (ROOT / other["source"]).read_text(encoding="utf-8").strip()
                assert other_body not in body


def test_assembly_records_every_section_once():
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / cfg["instructions"]["assembly"]).read_text(encoding="utf-8"))
    pairs = [(s["owner"], s["title"]) for s in manifest["sections"]]
    assert len(pairs) == len(set(pairs)) == 23
    assert set(manifest["sources"]) == {"core", *(s["id"] for s in cfg["skills"]["definitions"])}
