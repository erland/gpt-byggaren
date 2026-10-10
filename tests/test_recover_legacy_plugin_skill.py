import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(project):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/recover_legacy_plugin_skill.py"),
         "--project-root", str(project)], capture_output=True, text=True
    )


def test_missing_marknadskartlaggaren_skill_recovers_without_activation(tmp_path):
    instruction = tmp_path / "src/instructions/system.md"
    instruction.parent.mkdir(parents=True)
    original = "# Marknadskartläggaren\nGör aktuell webbresearch för marknadskartläggningar.\n".encode()
    instruction.write_bytes(original)
    cfg = {
        "instructions": {"canonical": "src/instructions/system.md"},
        "runtime": {"openai_plugin": {
            "enabled": True, "entrypoint": "skills/marknadskartlaggaren/SKILL.md",
        }},
    }
    config = tmp_path / "gpt-project.yaml"
    config.write_text(yaml.safe_dump(cfg))
    config_before = config.read_bytes()
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "review_required"
    assert report["source_sha256"] == hashlib.sha256(original).hexdigest()
    assert not report["plugin_activated"]
    assert not report["release_ready"]
    assert config.read_bytes() == config_before
    assert instruction.read_bytes() == original
    assert not (tmp_path / "skills/marknadskartlaggaren/SKILL.md").exists()
    generated = tmp_path / report["candidate"]
    text = generated.read_text()
    assert text.startswith("---\nname: marknadskartlaggaren\n")
    assert original.decode() in text
    assert run(tmp_path).returncode != 0


def test_blocks_existing_legacy_skill(tmp_path):
    instruction = tmp_path / "src/instructions/system.md"
    instruction.parent.mkdir(parents=True)
    instruction.write_text("Authoritative instructions")
    skill = tmp_path / "skills/marknadskartlaggaren/SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("Existing skill")
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump({
        "instructions": {"canonical": "src/instructions/system.md"},
        "runtime": {"openai_plugin": {"entrypoint": "skills/marknadskartlaggaren/SKILL.md"}}
    }))
    assert run(tmp_path).returncode != 0
    assert skill.read_text() == "Existing skill"
