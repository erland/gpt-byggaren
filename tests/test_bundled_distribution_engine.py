"""Offline distribution engine packaging regression checks."""
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def test_chat_and_plugin_bundle_engine(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_distributions.py"),
         "--project-root", str(ROOT), "--version", "0.0.0-test",
         "--targets", "chat,plugin"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for target in ("chat", "plugin"):
        archives = list((ROOT / "dist").glob(f"*{target}*0.0.0-test.zip"))
        assert archives, f"No archive for {target}"
        with zipfile.ZipFile(archives[0]) as archive:
            names = set(archive.namelist())
            assert "distribution-engine/scripts/build_distributions.py" in names
            assert "distribution-engine/scripts/install_distribution_engine.py" in names
            assert "distribution-engine/scripts/lib/project_model.py" in names
            assert "distribution-engine/templates/START-HERE.chat.md.tpl" in names


def test_bundled_engine_installs_and_builds_five_runtimes(tmp_path):
    import yaml

    version = "0.0.0-offline"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build_distributions.py"),
         "--project-root", str(ROOT), "--version", version,
         "--targets", "chat,plugin"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    archives = list((ROOT / "dist").glob(f"*plugin*{version}.zip"))
    assert len(archives) == 1
    extracted = tmp_path / "extracted"
    with zipfile.ZipFile(archives[0]) as archive:
        archive.extractall(extracted)
    engine = extracted / "distribution-engine"
    project = tmp_path / "generated"
    project.mkdir()
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    cfg["project"]["id"] = "offline-test"
    cfg["project"]["name"] = "Offline Test"
    (project / "gpt-project.yaml").write_text(
        yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8"
    )
    instruction = project / cfg["instructions"]["canonical"]
    instruction.parent.mkdir(parents=True, exist_ok=True)
    instruction.write_text("You are an offline test assistant.\n", encoding="utf-8")
    for skill in cfg["skills"]["definitions"]:
        for key in ("references", "assets", "scripts"):
            for item in skill.get(key, []):
                relative = item if isinstance(item, str) else item.get("path")
                if relative and (ROOT / relative).is_file():
                    dest = project / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes((ROOT / relative).read_bytes())
    install = subprocess.run(
        [sys.executable, str(engine / "scripts/install_distribution_engine.py"),
         "--source", str(engine), "--project-root", str(project)],
        capture_output=True, text=True,
    )
    assert install.returncode == 0, install.stdout + install.stderr
    built = subprocess.run(
        [sys.executable, str(project / "scripts/build_distributions.py"),
         "--project-root", str(project), "--version", "0.1.0",
         "--targets", "chat,plugin,claude_project,claude_skills,opencode"],
        capture_output=True, text=True,
    )
    assert built.returncode == 0, built.stdout + built.stderr
    outputs = list((project / "dist").glob("*.zip"))
    assert len(outputs) == 5
    with_names = []
    for output in outputs:
        with zipfile.ZipFile(output) as archive:
            with_names.append(frozenset(archive.namelist()))
    assert len(set(with_names)) == 5
