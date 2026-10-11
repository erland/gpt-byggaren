#!/usr/bin/env python3
"""Build canonical offline engine archive for the GitHub Release."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "dist" / "distribution-engine.zip"
PREFIXES = ("scripts", "templates", "schemas", "src")
FILES = [ROOT / "gpt-project.yaml"]
for prefix in PREFIXES:
    FILES.extend(p for p in (ROOT / prefix).rglob("*") if p.is_file()
                 and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pyo"})
TARGET.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(TARGET, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(FILES):
        info = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), (2020, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, p.read_bytes())
print(TARGET)
