"""
simple scorer: combines metric dict with weights from config.yaml
returns overall score (0-100) and the weighted breakdown per metric
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import yaml

from config_loader import cfg
C = cfg().get("weights", {})


# ──────────────────────── helpers ────────────────────────


def _default_weights() -> Dict[str, float]:
    """
    fallback weights if config.yaml misses some keys
    values are normalised so they always sum to 1.0
    """
    defaults = {
        "whitespace": 0.25,
        "contrast": 0.25,
        "color_harmony": 0.25,
        "text_density": 0.25,
    }
    # override with any values in config
    defaults.update({k: float(v) for k, v in C.items()})
    total = sum(defaults.values()) or 1.0
    return {k: v / total for k, v in defaults.items()}


_WEIGHTS = _default_weights()


# ───────────────────── public API ────────────────────────


def score_design(metrics: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    """
    metrics: dict from analyzer (0-100 each)
    returns (overall_score, breakdown), score rounded to 2 decimals
    """
    breakdown: Dict[str, float] = {}
    total = 0.0
    for key, value in metrics.items():
        weight = _WEIGHTS.get(key, 0.0)
        contrib = weight * value
        breakdown[key] = round(contrib, 2)
        total += contrib
    return round(total, 2), breakdown