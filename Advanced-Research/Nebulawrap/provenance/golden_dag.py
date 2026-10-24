# nebulawrap/provenance/golden_dag.py
import hashlib, json
from datetime import datetime

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"))

def make_golden_dag(decision_capsule: dict) -> str:
    """
    Deterministic 64-hex GoldenDAG id computed from canonicalized Decision Capsule.
    """
    payload = canonical_json({
        "ts": decision_capsule.get("timestamp"),
        "model": decision_capsule.get("model"),
        "prompt_hash": hashlib.sha256(decision_capsule.get("prompt","").encode()).hexdigest(),
        "meta": decision_capsule.get("meta",{})
    })
    return hashlib.sha256(payload.encode()).hexdigest()

def build_decision_capsule(prompt: str, model_meta: dict, response: str, extra=None):
    capsule = {
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "prompt": prompt,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "model": model_meta,
        "response_hash": hashlib.sha256((response or "").encode()).hexdigest(),
        "meta": extra or {}
    }
    capsule["golden_dag"] = make_golden_dag(capsule)
    return capsule
