from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from midipainter.config import ConvertConfig
from midipainter.image.contour import extract_contours, load_grayscale
from midipainter.mapping.notes import MappingLayout, Note, map_paths_to_note_mapping
from midipainter.midi.writer import write_midi
from midipainter.preview.debug import render_edge_preview
from midipainter.preview.piano_roll import render_piano_roll


@dataclass(frozen=True)
class ConvertResult:
    image_width: int
    image_height: int
    raw_contour_count: int
    contour_count: int
    rejected_by_points: int
    rejected_by_area: int
    contour_point_count: int
    note_count: int
    notes: list[Note]
    hit_note_limit: bool
    layout: MappingLayout


def convert_image_to_midi(
    image_path: str | Path,
    midi_path: str | Path | None,
    config: ConvertConfig,
    preview_path: str | Path | None = None,
    edge_preview_path: str | Path | None = None,
) -> ConvertResult:
    image = load_grayscale(image_path, config.max_width)
    height, width = image.shape[:2]
    paths, edges, stats = extract_contours(image, config)
    mapping = map_paths_to_note_mapping(paths, width, height, config)
    notes = mapping.notes
    if midi_path is not None:
        write_midi(notes, midi_path, config.ticks_per_beat)

    if preview_path is not None:
        total_ticks = int(round(config.total_beats * config.ticks_per_beat))
        render_piano_roll(
            notes,
            preview_path,
            config.min_pitch,
            config.max_pitch,
            total_ticks,
        )

    if edge_preview_path is not None:
        render_edge_preview(edges, edge_preview_path)

    return ConvertResult(
        width,
        height,
        stats.raw_count,
        len(paths),
        stats.rejected_by_points,
        stats.rejected_by_area,
        stats.sampled_point_count,
        len(notes),
        notes,
        config.max_notes > 0 and len(notes) >= config.max_notes,
        mapping.layout,
    )
