from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from midipainter.mapping.notes import Note


def render_piano_roll(
    notes: list[Note],
    output_path: str | Path,
    min_pitch: int,
    max_pitch: int,
    total_ticks: int,
    width: int = 1400,
    height: int = 720,
) -> None:
    output_path = Path(output_path)
    margin_left = 56
    margin_right = 24
    margin_top = 24
    margin_bottom = 40
    roll_w = width - margin_left - margin_right
    roll_h = height - margin_top - margin_bottom

    image = Image.new("RGB", (width, height), "#111318")
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        [margin_left, margin_top, margin_left + roll_w, margin_top + roll_h],
        fill="#181b22",
        outline="#303744",
    )

    pitch_count = max(1, max_pitch - min_pitch + 1)
    for pitch in range(min_pitch, max_pitch + 1):
        y = margin_top + (max_pitch - pitch) / max(1, pitch_count - 1) * roll_h
        color = "#242936" if pitch % 12 in (0, 2, 4, 5, 7, 9, 11) else "#202530"
        draw.line([margin_left, y, margin_left + roll_w, y], fill=color)
        if pitch % 12 == 0:
            draw.text((8, y - 6), f"C{pitch // 12 - 1}", fill="#9aa4b2")

    beats = max(1, round(total_ticks / 480))
    for beat in range(beats + 1):
        x = margin_left + beat / beats * roll_w
        color = "#3b4352" if beat % 4 == 0 else "#282e39"
        draw.line([x, margin_top, x, margin_top + roll_h], fill=color)
        if beat % 4 == 0:
            draw.text((x + 4, margin_top + roll_h + 10), str(beat // 4 + 1), fill="#9aa4b2")

    for note in notes:
        if note.pitch < min_pitch or note.pitch > max_pitch:
            continue
        x1 = margin_left + note.start_tick / max(1, total_ticks) * roll_w
        x2 = margin_left + (note.start_tick + note.duration_ticks) / max(1, total_ticks) * roll_w
        y = margin_top + (max_pitch - note.pitch) / max(1, pitch_count - 1) * roll_h
        note_h = max(3, roll_h / pitch_count * 0.72)
        draw.rectangle(
            [x1, y - note_h / 2, max(x1 + 2, x2), y + note_h / 2],
            fill="#43d6a1",
            outline="#b7ffe4",
        )

    draw.text((margin_left, 4), f"MidiPainter preview - {len(notes)} notes", fill="#d5d9e2")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
