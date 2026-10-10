import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_host_skill_readiness import check


def _package(tmp_path, target):
    base = tmp_path / target
    folder = base / "skills" / "example"
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text("---\nname: example\ndescription: Does an example\n---\nUse this skill.")
    if target == "plugin":
        (base / "plugin.json").write_text("{}")
    else:
        (base / "project").mkdir()
    return base


def test_offline_preflight_for_both_hosts(tmp_path):
    for target in ("plugin", "claude"):
        result = check(_package(tmp_path, target), target)
        assert result["status"] == "offline_ready"
        assert result["host_installed"] is False
        assert result["host_execution_verified"] is False


def test_plugin_rejects_nested_mcp_config(tmp_path):
    base = _package(tmp_path, "plugin")
    (base / "skills" / "example" / "mcp.json").write_text("{}")
    assert check(base, "plugin")["status"] == "invalid"


def test_host_rejects_invalid_skill_frontmatter(tmp_path):
    base = _package(tmp_path, "claude")
    (base / "skills" / "example" / "SKILL.md").write_text("missing metadata")
    assert check(base, "claude")["status"] == "invalid"
