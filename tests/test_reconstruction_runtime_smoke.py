import importlib.util
import json
from pathlib import Path
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "smoke_test_reconstructed_distributions",
    ROOT / "scripts/smoke_test_reconstructed_distributions.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def project(tmp_path):
    file = tmp_path / "src/instructions/system.md"
    file.parent.mkdir(parents=True)
    file.write_bytes(b"Original behavior")
    (tmp_path / "gpt-project.yaml").write_text(yaml.safe_dump({
        "instructions": {"canonical": "src/instructions/system.md"},
        "reconstruction": {"release_ready": False, "status": "canonical_contracts_scaffolded"},
    }))
    return file.read_bytes()


def pack(tmp_path, name, entries):
    target = tmp_path / name
    with zipfile.ZipFile(target, "w") as archive:
        for path, content in entries.items():
            archive.writestr(path, content)
    return target


def test_chat_package_checks_instruction_and_says_not_release_ready(tmp_path):
    instructions = project(tmp_path)
    manifest = {"files": [{"path": "assistant/instructions.md", "sha256": __import__("hashlib").sha256(instructions).hexdigest()}]}
    archive = pack(tmp_path, "chat.zip", {
        "assistant/instructions.md": instructions,
        "START-HERE.md": "Start", "VERSION": "1.0",
        "MANIFEST.json": json.dumps(manifest),
    })
    report = module.evaluate(tmp_path, {"chat": archive})
    assert report["result"] == "offline_checks_passed"
    assert report["functional_parity_verified"] is False
    assert report["release_ready"] is False


def test_detects_instruction_drift_and_manifest_tampering(tmp_path):
    project(tmp_path)
    archive = pack(tmp_path, "chat.zip", {
        "assistant/instructions.md": "Changed", "START-HERE.md": "Start",
        "VERSION": "1", "MANIFEST.json": json.dumps({"files": [
            {"path": "assistant/instructions.md", "sha256": "broken"}]}),
    })
    issues = module.evaluate(tmp_path, {"chat": archive})["runtimes"]["chat"]["issues"]
    assert any("instruction mismatch" in issue for issue in issues)
    assert any("checksum mismatch" in issue for issue in issues)


def test_nested_mcp_json_is_forbidden_in_plugin(tmp_path):
    project(tmp_path)
    archive = pack(tmp_path, "plugin.zip", {
        "plugin.json": "{}", "nested/mcp.json": "{}",
    })
    report = module.evaluate(tmp_path, {"plugin": archive})
    assert any("mcp.json" in reason for reason in report["runtimes"]["plugin"]["issues"])
    assert report["release_ready"] is False
