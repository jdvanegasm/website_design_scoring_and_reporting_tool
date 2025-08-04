from pathlib import Path
from functools import lru_cache
from typing import Any, Dict
import yaml


@lru_cache
def cfg() -> Dict[str, Any]:
    f = Path("../config.yaml")
    if f.exists():
        return yaml.safe_load(f.read_text()) or {}
    return {}