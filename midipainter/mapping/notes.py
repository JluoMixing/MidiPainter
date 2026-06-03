from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, NamedTuple

from midipainter.config import ConvertConfig
from midipainter.image.contour import PathPoints


@dataclass(frozen=True, order=True)
class Note:
    start_tick: int
    pitch: int
    duration_ticks: int
    velocity: int


class MappingLayout(NamedTuple):
    x_offset: float
    y_offset: float
    x_scale: float
    y_scale: float
    aspect_mode: str
    display_aspect: float


class NoteMapping(NamedTuple):
    notes: list[Note]
    layout: MappingLayout


def _quantize_tick(tick: float, grid_ticks: int) -> int:
    if grid_ticks <= 0:
        return int(round(tick))
    return int(round(tick / grid_ticks) * grid_ticks)


def _build_layout(image_width: int, image_height: int, config: ConvertConfig) -> MappingLayout:
    mode = config.aspect_mode.lower()
    display_aspect = max(0.001, config.display_aspect)
    if mode == "stretch" or image_width <= 0 or image_height <= 0:
        return MappingLayout(0.0, 0.0, 1.0, 1.0, mode, display_aspect)

    if mode != "contain":
        raise ValueError(f"Unsupported aspect mode: {config.aspect_mode}")

    source_aspect = image_width / image_height
    if source_aspect > display_aspect:
        y_scale = display_aspect / source_aspect
        return MappingLayout(0.0, (1.0 - y_scale) / 2.0, 1.0, y_scale, mode, display_aspect)

    x_scale = source_aspect / display_aspect
    return MappingLayout((1.0 - x_scale) / 2.0, 0.0, x_scale, 1.0, mode, display_aspect)


def map_paths_to_notes(
    paths: Iterable[PathPoints],
    image_width: int,
    image_height: int,
    config: ConvertConfig,
) -> list[Note]:
    return map_paths_to_note_mapping(paths, image_width, image_height, config).notes


def map_paths_to_note_mapping(
    paths: Iterable[PathPoints],
    image_width: int,
    image_height: int,
    config: ConvertConfig,
) -> NoteMapping:
    path_list = list(paths)
    layout = _build_layout(image_width, image_height, config)
    max_tick = int(round(config.total_beats * config.ticks_per_beat))
    duration = max(1, int(round(config.note_beats * config.ticks_per_beat)))
    grid = max(1, int(round(config.quantize_beats * config.ticks_per_beat)))
    pitch_span = max(1, config.max_pitch - config.min_pitch)
    sample_step = max(1, config.sample_step)
    if config.auto_sample and config.max_notes > 0:
        estimated_points = sum((len(path) + sample_step - 1) // sample_step for path in path_list)
        if estimated_points > config.max_notes:
            multiplier = (estimated_points + config.max_notes - 1) // config.max_notes
            sample_step *= max(1, multiplier)

    dedup: dict[tuple[int, int], Note] = {}
    for path in path_list:
        for x, y in path[::sample_step]:
            raw_nx = 0.0 if image_width <= 1 else x / (image_width - 1)
            raw_ny = 0.0 if image_height <= 1 else y / (image_height - 1)
            nx = layout.x_offset + raw_nx * layout.x_scale
            ny = layout.y_offset + raw_ny * layout.y_scale
            tick = _quantize_tick(nx * max_tick, grid)
            pitch = int(round(config.max_pitch - ny * pitch_span))
            pitch = max(0, min(127, pitch))
            tick = max(0, min(max_tick, tick))
            key = (tick, pitch)
            dedup[key] = Note(tick, pitch, duration, config.velocity)

    notes = sorted(dedup.values())
    if len(notes) <= config.max_notes:
        return NoteMapping(notes, layout)

    stride = max(1, (len(notes) + config.max_notes - 1) // config.max_notes)
    limited = notes[::stride]
    return NoteMapping(limited[: config.max_notes], layout)
