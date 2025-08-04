"""
design analyzer: extracts simple, fast metrics from a homepage screenshot.

returns a dict where every metric is normalised to 0-100
so that scorer.py can combine them with weights from config.yaml.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import cv2
import numpy as np
from PIL import Image

from config_loader import cfg
C = cfg().get("analyzer", {})


# ──────────────────────── helpers ────────────────────────


def _load_image(path: Path) -> np.ndarray:
    """
    loads a png or jpeg screenshot and returns an opencv bgr array.
    if the image has an alpha channel, it is composited over white
    this is a way to avoid all-black pixels that break the metrics.
    """
    pil_img = Image.open(path)
    if pil_img.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", pil_img.size, (255, 255, 255, 255))
        pil_img = Image.alpha_composite(bg, pil_img).convert("RGB")
    else:
        pil_img = pil_img.convert("RGB")

    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def _get_whitespace_ratio(img_bgr: np.ndarray, tol: int) -> float:
    """
    approximate whitespace as pixels that are very light (R,G,B > tol) 
    or very dark, all < 10. Returns % 0-1. (but dark ones are not really counted as whitespaces)
    """
    mask_light = np.all(img_bgr > tol, axis=2)
    return float(np.sum(mask_light)) / img_bgr.shape[0] / img_bgr.shape[1]


def _get_contrast_score(img_grey: np.ndarray, p_low: int, p_high: int) -> float:
    """
    uses 90th-10th percentile luminance difference as a crude contrast proxy (0-255 to map to 0-100).
    """
    p1, p2 = np.percentile(img_grey, [p_low, p_high])
    diff = p2 - p1
    return float(np.clip(diff / 200 * 100, 0, 100))


def _dominant_colors(img_bgr: np.ndarray, k: int = 5) -> np.ndarray:
    """
    k-Means on a down-sampled image to find dominant palette (BGR centroids).
    """
    small = cv2.resize(img_bgr, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
    data = small.reshape((-1, 3)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, _, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    return centers.astype(int)


def _palette_harmony_score(centers: np.ndarray) -> float:
    """
    this is a gross metric (i think it could be enhanced for a production phase): 
    penalise palettes whose centroids are evenly spaced
    (meaning that there are many colors) and reward palettes with related colors.
    Compute hue distance matrix in hsv and use its variance.
    """
    hsv = cv2.cvtColor(np.uint8(centers[np.newaxis, ...]), cv2.COLOR_BGR2HSV)[0]
    hues = hsv[:, 0].astype(float)

    diff_matrix = np.abs(hues[:, None] - hues[None, :])
    diff_matrix = np.minimum(diff_matrix, 180 - diff_matrix)
    variance = np.var(diff_matrix)

    return float(np.clip(100 - (variance / 50), 0, 100))


def _text_density_score(img_grey: np.ndarray, lo: float, hi: float) -> float:
    """
    canny test as strong intensity transitions:
    canny edge density as proxy, cause lots of edges likely means text/images clutter.
    i assume 5-20 % edge pixels is ideal then map to 100.
    """
    edges = cv2.Canny(img_grey, 100, 200)
    ratio = np.mean(edges > 0)

    if ratio < lo:        # too sparse
        return ratio / lo * 60
    if ratio > hi:        # too noisy
        return max(20, 100 - (ratio - hi) / 0.30 * 80)
    return 100.0          # ideal


# ───────────────────── public API ────────────────────────


def analyze_design(img_path: Path) -> Dict[str, float]:
    """
    returns normalised metrics (0-100):
        • whitespace
        • contrast
        • color_harmony
        • text_density
    i think it can be extend with more metrics as needed, this is just a demo.
    """
    img_bgr = _load_image(img_path)
    img_grey = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    tol = C.get("whitespace_tol", 245)
    whitespace_ratio = _get_whitespace_ratio(img_bgr, tol)
    whitespace_score = float(np.clip((whitespace_ratio / 0.60) * 100, 0, 100))

    p_low, p_high = C.get("contrast_percentiles", [5, 95])
    contrast_score = _get_contrast_score(img_grey, p_low, p_high)

    palette = _dominant_colors(img_bgr, k=5)
    color_harmony_score = _palette_harmony_score(palette)

    lo, hi = C.get("edge_ratio_ideal", [0.05, 0.20])
    text_density_score = _text_density_score(img_grey, lo, hi)

    return {
        "whitespace": round(whitespace_score, 2),
        "contrast": round(contrast_score, 2),
        "color_harmony": round(color_harmony_score, 2),
        "text_density": round(text_density_score, 2),
    }