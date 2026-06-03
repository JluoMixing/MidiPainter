from __future__ import annotations

from pathlib import Path

from midipainter.mapping.notes import Note


def _var_len(value: int) -> bytes:
    value = max(0, int(value))
    buffer = value & 0x7F
    value >>= 7
    while value:
        buffer <<= 8
        buffer |= (value & 0x7F) | 0x80
        value >>= 7

    out = bytearray()
    while True:
        out.append(buffer & 0xFF)
        if buffer & 0x80:
            buffer >>= 8
        else:
            break
    return bytes(out)


def write_midi(
    notes: list[Note],
    output_path: str | Path,
    ticks_per_beat: int = 480,
    tempo_bpm: int = 120,
) -> None:
    output_path = Path(output_path)
    events: list[tuple[int, int, bytes]] = []

    for note in notes:
        pitch = max(0, min(127, note.pitch))
        velocity = max(1, min(127, note.velocity))
        start = max(0, note.start_tick)
        end = start + max(1, note.duration_ticks)
        events.append((start, 1, bytes([0x90, pitch, velocity])))
        events.append((end, 0, bytes([0x80, pitch, 0])))

    events.sort()

    tempo = int(60_000_000 / max(1, tempo_bpm))
    track = bytearray()
    track.extend(b"\x00\xff\x51\x03")
    track.extend(tempo.to_bytes(3, "big"))
    track.extend(b"\x00\xff\x58\x04\x04\x02\x18\x08")

    last_tick = 0
    for tick, _, payload in events:
        track.extend(_var_len(tick - last_tick))
        track.extend(payload)
        last_tick = tick

    track.extend(b"\x00\xff\x2f\x00")

    header = b"MThd" + (6).to_bytes(4, "big")
    header += (0).to_bytes(2, "big")
    header += (1).to_bytes(2, "big")
    header += int(ticks_per_beat).to_bytes(2, "big")

    chunk = b"MTrk" + len(track).to_bytes(4, "big") + bytes(track)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(header + chunk)
