from __future__ import annotations

import argparse
from pathlib import Path

from midipainter.config import ConvertConfig
from midipainter.pipeline.convert import convert_image_to_midi


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="midipainter",
        description="Convert image contours into MIDI piano roll patterns.",
    )
    parser.add_argument("image", type=Path, help="Input image path.")
    parser.add_argument("midi", type=Path, help="Output MIDI file path.")
    parser.add_argument("--preview", type=Path, help="Optional piano roll preview PNG path.")
    parser.add_argument("--edge-preview", type=Path, help="Optional edge detection preview PNG path.")
    parser.add_argument("--min-pitch", type=int, default=36)
    parser.add_argument("--max-pitch", type=int, default=96)
    parser.add_argument("--total-beats", type=float, default=64.0)
    parser.add_argument("--note-beats", type=float, default=0.125)
    parser.add_argument("--quantize-beats", type=float, default=0.125)
    parser.add_argument("--velocity", type=int, default=84)
    parser.add_argument("--aspect-mode", choices=["contain", "stretch"], default="contain")
    parser.add_argument(
        "--display-aspect",
        type=float,
        default=2.012,
        help="Physical piano-roll width/height ratio used by contain mode.",
    )
    parser.add_argument("--max-width", type=int, default=512)
    parser.add_argument("--canny-low", type=int, default=80)
    parser.add_argument("--canny-high", type=int, default=180)
    parser.add_argument("--min-contour-points", type=int, default=4)
    parser.add_argument("--min-contour-area", type=float, default=8.0)
    parser.add_argument("--max-contours", type=int, default=512)
    parser.add_argument("--simplify-epsilon", type=float, default=1.5)
    parser.add_argument("--sample-step", type=int, default=2)
    parser.add_argument("--no-auto-sample", action="store_true")
    parser.add_argument("--max-notes", type=int, default=5000)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = ConvertConfig(
        min_pitch=args.min_pitch,
        max_pitch=args.max_pitch,
        total_beats=args.total_beats,
        note_beats=args.note_beats,
        quantize_beats=args.quantize_beats,
        velocity=args.velocity,
        aspect_mode=args.aspect_mode,
        display_aspect=args.display_aspect,
        max_width=args.max_width,
        canny_low=args.canny_low,
        canny_high=args.canny_high,
        min_contour_points=args.min_contour_points,
        min_contour_area=args.min_contour_area,
        max_contours=args.max_contours,
        simplify_epsilon=args.simplify_epsilon,
        sample_step=args.sample_step,
        auto_sample=not args.no_auto_sample,
        max_notes=args.max_notes,
    )

    result = convert_image_to_midi(
        args.image,
        args.midi,
        config,
        args.preview,
        args.edge_preview,
    )
    print(f"Image: {result.image_width}x{result.image_height}")
    print(f"Raw contours: {result.raw_contour_count}")
    print(f"Kept contours: {result.contour_count}")
    print(f"Rejected by points: {result.rejected_by_points}")
    print(f"Rejected by area: {result.rejected_by_area}")
    print(f"Contour points: {result.contour_point_count}")
    print(f"Notes: {result.note_count}")
    print(f"Aspect mode: {result.layout.aspect_mode}")
    print(f"Layout x: offset={result.layout.x_offset:.3f}, scale={result.layout.x_scale:.3f}")
    print(f"Layout y: offset={result.layout.y_offset:.3f}, scale={result.layout.y_scale:.3f}")
    if result.hit_note_limit:
        print(f"Note limit hit: {config.max_notes}")
    print(f"MIDI: {args.midi}")
    if args.preview:
        print(f"Preview: {args.preview}")
    if args.edge_preview:
        print(f"Edge preview: {args.edge_preview}")
    return 0
