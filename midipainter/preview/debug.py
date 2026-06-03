from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def render_edge_preview(edges: np.ndarray, output_path: str | Path) -> None:
    output_path = Path(output_path)
    image = Image.fromarray(edges).convert("L")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
