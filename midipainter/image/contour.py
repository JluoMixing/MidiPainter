from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np

from midipainter.config import ConvertConfig

Point = Tuple[int, int]
PathPoints = List[Point]


class ContourStats:
    def __init__(
        self,
        raw_count: int,
        kept_count: int,
        rejected_by_points: int,
        rejected_by_area: int,
        sampled_point_count: int,
    ) -> None:
        self.raw_count = raw_count
        self.kept_count = kept_count
        self.rejected_by_points = rejected_by_points
        self.rejected_by_area = rejected_by_area
        self.sampled_point_count = sampled_point_count


def load_grayscale(path: str | Path, max_width: int) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Could not load image: {path}")

    if image.ndim == 3 and image.shape[2] == 4:
        alpha = image[:, :, 3]
        rgb = image[:, :, :3]
        white = np.full_like(rgb, 255)
        alpha_f = alpha[:, :, None].astype(np.float32) / 255.0
        image = (rgb * alpha_f + white * (1.0 - alpha_f)).astype(np.uint8)

    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = image.shape[:2]
    if width > max_width:
        scale = max_width / width
        image = cv2.resize(
            image,
            (max_width, max(1, int(height * scale))),
            interpolation=cv2.INTER_AREA,
        )

    return image


def extract_contours(
    image: np.ndarray,
    config: ConvertConfig,
) -> tuple[list[PathPoints], np.ndarray, ContourStats]:
    blur_size = max(1, config.blur)
    if blur_size % 2 == 0:
        blur_size += 1

    blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
    edges = cv2.Canny(blurred, config.canny_low, config.canny_high)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    paths: list[PathPoints] = []
    rejected_by_points = 0
    rejected_by_area = 0
    for contour in contours:
        if len(contour) < config.min_contour_points:
            rejected_by_points += 1
            continue

        area = cv2.contourArea(contour)
        if area < config.min_contour_area:
            rejected_by_area += 1
            continue

        simplified = cv2.approxPolyDP(contour, config.simplify_epsilon, False)
        points = [(int(point[0][0]), int(point[0][1])) for point in simplified]
        if len(points) >= config.min_contour_points:
            paths.append(points)
        else:
            rejected_by_points += 1

    paths.sort(key=len, reverse=True)
    if config.max_contours > 0:
        paths = paths[: config.max_contours]

    stats = ContourStats(
        raw_count=len(contours),
        kept_count=len(paths),
        rejected_by_points=rejected_by_points,
        rejected_by_area=rejected_by_area,
        sampled_point_count=sum(len(path) for path in paths),
    )
    return paths, edges, stats
