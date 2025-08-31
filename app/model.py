import os
from typing import Any, List, Tuple

import joblib

_MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/iris_clf.joblib")
_model = None
_target_names: List[str] | None = None


def load_model() -> Tuple[Any, list[str]]:
    global _model, _target_names
    if _model is None or _target_names is None:
        bundle = joblib.load(_MODEL_PATH)
        _model = bundle["model"]
        _target_names = bundle["target_names"]
    return _model, _target_names
