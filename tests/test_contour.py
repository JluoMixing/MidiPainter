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
