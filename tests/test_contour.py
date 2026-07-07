import pytest
from PIL import Image
import numpy as np

from midipainter.config import ConvertConfig
from midipainter.image.contour import extract_contours


def test_extract_contours_reports_rejections_for_tiny_noise():
    image = np.full((80, 80), 255, dtype=np.uint8)
    image[10, 10] = 0
    image[30:60, 30:60] = 0

    paths, _, stats = extract_contours(
        image,
        ConvertConfig(max_width=80, min_contour_area=20.0),
    )

    assert len(paths) > 0
    assert stats.raw_count >= stats.kept_count
    assert stats.rejected_by_area > 0


def test_load_grayscale_supports_unicode_paths(tmp_path):
    from midipainter.image.contour import load_grayscale

    image_path = tmp_path / "\u4e2d\u6587\u56fe\u7247.png"
    Image.new("RGB", (24, 12), "white").save(image_path)

    image = load_grayscale(image_path, max_width=24)

    assert image.shape == (12, 24)


def test_load_grayscale_reports_missing_unicode_path(tmp_path):
    from midipainter.image.contour import load_grayscale

    with pytest.raises(ValueError, match="Could not load image"):
        load_grayscale(tmp_path / "\u4e0d\u5b58\u5728.png", max_width=24)
