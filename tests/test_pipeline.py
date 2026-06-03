from PIL import Image, ImageDraw

from midipainter.config import ConvertConfig
from midipainter.pipeline.convert import convert_image_to_midi


def test_convert_image_to_midi_creates_midi_and_preview(tmp_path):
    image_path = tmp_path / "shape.png"
    midi_path = tmp_path / "shape.mid"
    preview_path = tmp_path / "shape_preview.png"
    edge_preview_path = tmp_path / "shape_edges.png"

    image = Image.new("RGB", (160, 100), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([24, 20, 136, 80], outline="black", width=3)
    image.save(image_path)

    result = convert_image_to_midi(
        image_path,
        midi_path,
        ConvertConfig(max_width=160, max_notes=1000),
        preview_path,
        edge_preview_path,
    )

    assert result.note_count > 0
    assert result.raw_contour_count >= result.contour_count
    assert midi_path.exists()
    assert preview_path.exists()
    assert edge_preview_path.exists()
