from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertConfig:
    min_pitch: int = 36
    max_pitch: int = 96
    total_beats: float = 64.0
    ticks_per_beat: int = 480
    note_beats: float = 0.125
    quantize_beats: float = 0.125
    velocity: int = 84
    aspect_mode: str = "contain"
    display_aspect: float = 2.012
    max_width: int = 512
    blur: int = 3
    canny_low: int = 80
    canny_high: int = 180
    min_contour_points: int = 4
    min_contour_area: float = 8.0
    max_contours: int = 512
    simplify_epsilon: float = 1.5
    sample_step: int = 2
    auto_sample: bool = True
    max_notes: int = 5000
