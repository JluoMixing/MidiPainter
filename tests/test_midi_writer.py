from midipainter.mapping.notes import Note
from midipainter.midi.writer import write_midi


def test_write_midi_creates_standard_header(tmp_path):
    path = tmp_path / "out.mid"
    write_midi([Note(0, 60, 120, 80)], path)

    data = path.read_bytes()
    assert data.startswith(b"MThd")
    assert b"MTrk" in data
