from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def load_e2e_module():
    path = ROOT / "scripts" / "run_e2e_blank_idea.py"
    spec = importlib.util.spec_from_file_location("run_e2e_blank_idea", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_model_robustness_inference_is_adaptive():
    module = load_e2e_module()

    lightweight = module.infer_model_robustness({})
    guided = module.infer_model_robustness({"moderate_workflow": True})
    stateful = module.infer_model_robustness({"research_heavy": True})

    assert lightweight["level"] == "lightweight"
    assert lightweight["operational_core"] is False
    assert lightweight["explicit_workflow"] is False
    assert lightweight["model_compatibility_evals"] is False

    assert guided["level"] == "guided"
    assert guided["operational_core"] is True
    assert guided["explicit_workflow"] is False
    assert guided["model_compatibility_evals"] is True

    assert stateful["level"] == "stateful"
    assert stateful["operational_core"] is True
    assert stateful["explicit_workflow"] is True
    assert stateful["deterministic_gates"] is True
    assert stateful["model_compatibility_evals"] is True


def test_generated_gpt_robustness_policy_prefers_minimum_sufficient_level():
    policy = (ROOT / "src" / "runtime-policy" / "generated-gpt-model-robustness-policy.md").read_text(encoding="utf-8")

    assert "Välj minsta nivå" in policy
    assert "lightweight" in policy
    assert "guided" in policy
    assert "stateful" in policy
    assert "Luna-" in policy
