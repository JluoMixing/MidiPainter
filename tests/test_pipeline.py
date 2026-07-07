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


def test_convert_image_to_midi_supports_unicode_paths(tmp_path):
    unicode_dir = tmp_path / "\u4e2d\u6587\u76ee\u5f55"
    unicode_dir.mkdir()
    image_path = unicode_dir / "\u5f62\u72b6.png"
    midi_path = unicode_dir / "\u8f93\u51fa.mid"
    preview_path = unicode_dir / "\u9884\u89c8.png"
    edge_preview_path = unicode_dir / "\u8fb9\u7f18.png"

    image = Image.new("RGB", (120, 90), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse([24, 18, 96, 72], outline="black", width=3)
    image.save(image_path)

    result = convert_image_to_midi(
        image_path,
        midi_path,
        ConvertConfig(max_width=120, max_notes=1000),
        preview_path,
        edge_preview_path,
    )

    assert result.note_count > 0
    assert midi_path.exists()
    assert preview_path.exists()
    assert edge_preview_path.exists()
