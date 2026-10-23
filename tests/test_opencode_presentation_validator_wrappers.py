"""Regression: projected OpenCode validators must accept an explicit target file."""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("engine_builder", ROOT / "scripts" / "build_distributions.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_presentation_plan_wrapper_passes_required_file():
    output = module._opencode_tool_wrapper({"id":"presentation_plan_validate","purpose":"Validate plan"},"scripts/validate_presentation_plan.py")
    assert 'file: tool.schema.string().min(1)' in output
    assert 'const cmd = ["python3", script, file]' in output
    assert 'path.relative(projectRoot, file)' in output

def test_pptx_wrapper_passes_required_file():
    output = module._opencode_tool_wrapper({"id":"pptx_validate","purpose":"Validate pptx"},"scripts/validate_pptx.py")
    assert 'file: tool.schema.string().min(1)' in output
    assert 'const cmd = ["python3", script, file]' in output

def test_unrecognized_script_does_not_get_fictitious_flags():
    output = module._opencode_tool_wrapper({"id":"unknown_script","purpose":"Unknown"},"scripts/x.py")
    assert 'const cmd = ["python3", script]' in output
