from midipainter.config import ConvertConfig
from midipainter.mapping.notes import map_paths_to_note_mapping, map_paths_to_notes


def test_map_paths_to_notes_deduplicates_and_bounds_pitch():
    config = ConvertConfig(
        min_pitch=40,
        max_pitch=50,
        total_beats=4,
        max_notes=10,
        aspect_mode="stretch",
    )
    notes = map_paths_to_notes([[(0, 0), (0, 0), (99, 99)]], 100, 100, config)

    assert len(notes) == 2
    assert notes[0].pitch == 50
    assert notes[-1].pitch == 40
    assert notes[-1].start_tick == 4 * config.ticks_per_beat


def test_map_paths_to_notes_respects_max_notes_with_auto_sample():
    path = [(x, x % 100) for x in range(1000)]
    config = ConvertConfig(
        min_pitch=36,
        max_pitch=96,
        total_beats=16,
        sample_step=1,
        max_notes=50,
        auto_sample=True,
    )

    notes = map_paths_to_notes([path], 1000, 100, config)

    assert len(notes) <= 50


def test_contain_aspect_mode_preserves_tall_image_shape_with_horizontal_padding():
    config = ConvertConfig(
        min_pitch=36,
        max_pitch=96,
        total_beats=16,
        aspect_mode="contain",
        display_aspect=2.0,
        sample_step=1,
    )

    mapping = map_paths_to_note_mapping([[(0, 0), (99, 199)]], 100, 200, config)

    assert mapping.layout.x_offset > 0
    assert mapping.layout.x_scale < 1
    assert mapping.layout.y_offset == 0
    assert mapping.layout.y_scale == 1
    assert mapping.notes[0].start_tick > 0
    assert mapping.notes[-1].start_tick < 16 * config.ticks_per_beat


def test_stretch_aspect_mode_uses_full_timeline():
    config = ConvertConfig(
        min_pitch=36,
        max_pitch=96,
        total_beats=16,
        aspect_mode="stretch",
        sample_step=1,
    )

    mapping = map_paths_to_note_mapping([[(0, 0), (99, 199)]], 100, 200, config)

    assert mapping.layout.x_offset == 0
    assert mapping.layout.x_scale == 1
    assert mapping.notes[0].start_tick == 0
    assert mapping.notes[-1].start_tick == 16 * config.ticks_per_beat
