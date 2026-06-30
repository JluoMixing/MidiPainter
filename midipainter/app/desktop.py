from __future__ import annotations

import tempfile
import threading
from pathlib import Path
from tkinter import (
    BooleanVar,
    DoubleVar,
    IntVar,
    StringVar,
    Tk,
    filedialog,
    messagebox,
)
from tkinter import ttk

from PIL import Image, ImageTk

from midipainter.config import ConvertConfig
from midipainter.pipeline.convert import ConvertResult, convert_image_to_midi


class MidiPainterApp:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("MidiPainter")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)

        self.input_path = StringVar()
        self.output_path = StringVar(value=str(Path.cwd() / "output.mid"))
        self.preview_path = StringVar(value=str(Path.cwd() / "preview.png"))
        self.edge_preview_path = StringVar(value=str(Path.cwd() / "edges.png"))
        self.status = StringVar(value="Choose an image to begin.")
        self.stats = StringVar(value="No conversion yet.")

        self.min_pitch = IntVar(value=36)
        self.max_pitch = IntVar(value=96)
        self.total_beats = DoubleVar(value=64.0)
        self.detail = IntVar(value=58)
        self.aspect_mode = StringVar(value="contain")
        self.edge_preview_enabled = BooleanVar(value=True)
        self.detail_label = StringVar()
        self.detail_hint = StringVar()

        self._input_photo: ImageTk.PhotoImage | None = None
        self._roll_photo: ImageTk.PhotoImage | None = None
        self._busy = False
        self._preview_after_id: str | None = None

        self._configure_style()
        self._build_ui()
        self._sync_detail_text()
        self.detail.trace_add("write", self._detail_changed)

    def _configure_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        self.root.configure(bg="#f4f1ea")
        style.configure(".", background="#f4f1ea", foreground="#2d302b", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f4f1ea")
        style.configure("Panel.TFrame", background="#fffdf8", relief="flat")
        style.configure("TLabel", background="#f4f1ea", foreground="#2d302b")
        style.configure("Muted.TLabel", foreground="#72766e")
        style.configure("Panel.TLabel", background="#fffdf8", foreground="#2d302b")
        style.configure("PanelMuted.TLabel", background="#fffdf8", foreground="#72766e")
        style.configure("Title.TLabel", background="#f4f1ea", foreground="#26322d", font=("Segoe UI", 19, "bold"))
        style.configure("Section.TLabel", background="#fffdf8", foreground="#26322d", font=("Segoe UI", 11, "bold"))
        style.configure("Value.TLabel", background="#fffdf8", foreground="#30594f", font=("Segoe UI", 11, "bold"))
        style.configure("TButton", background="#ece7dc", foreground="#2d302b", borderwidth=0, padding=(12, 8))
        style.map("TButton", background=[("active", "#e1dacd")])
        style.configure("Accent.TButton", background="#416b60", foreground="#fffdf8")
        style.map("Accent.TButton", background=[("active", "#4f7c70")])
        style.configure("TEntry", fieldbackground="#f8f5ee", foreground="#2d302b", bordercolor="#d7d0c2")
        style.configure("TCombobox", fieldbackground="#f8f5ee", foreground="#2d302b")
        style.configure("TCheckbutton", background="#fffdf8", foreground="#2d302b")
        style.configure("Horizontal.TScale", background="#fffdf8", troughcolor="#e1dacd")

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="MidiPainter", style="Title.TLabel").pack(side="left")
        ttk.Label(
            header,
            text="Turn image contours into quiet, precise piano-roll patterns",
            style="Muted.TLabel",
        ).pack(side="left", padx=(14, 0), pady=(6, 0))

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        preview_panel = ttk.Frame(body, style="Panel.TFrame", padding=14)
        preview_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        preview_panel.rowconfigure(1, weight=1)
        preview_panel.columnconfigure(0, weight=1)

        file_bar = ttk.Frame(preview_panel, style="Panel.TFrame")
        file_bar.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Button(file_bar, text="Open Image", command=self.choose_image).pack(side="left")
        ttk.Button(file_bar, text="Preview Only", command=self.preview_only).pack(side="left", padx=(8, 0))
        ttk.Button(file_bar, text="Convert MIDI", style="Accent.TButton", command=self.convert).pack(side="left", padx=(8, 0))

        image_area = ttk.Frame(preview_panel, style="Panel.TFrame")
        image_area.grid(row=1, column=0, sticky="nsew")
        image_area.columnconfigure(0, weight=1)
        image_area.columnconfigure(1, weight=1)
        image_area.rowconfigure(1, weight=1)
        ttk.Label(image_area, text="Input", style="Panel.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(image_area, text="Piano Roll Preview", style="Panel.TLabel").grid(row=0, column=1, sticky="w")
        self.input_preview = ttk.Label(image_area, text="No image", style="Muted.TLabel", anchor="center")
        self.input_preview.grid(row=1, column=0, sticky="nsew", padx=(0, 8), pady=(8, 0))
        self.roll_preview = ttk.Label(image_area, text="No preview", style="Muted.TLabel", anchor="center")
        self.roll_preview.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=(8, 0))

        side = ttk.Frame(body, style="Panel.TFrame", padding=14)
        side.grid(row=0, column=1, sticky="nsew")
        side.columnconfigure(1, weight=1)

        row = 0
        row = self._path_row(side, row, "MIDI", self.output_path, self.choose_midi_save)
        row = self._path_row(side, row, "Preview", self.preview_path, self.choose_preview_save)
        row = self._path_row(side, row, "Edges", self.edge_preview_path, self.choose_edge_save)

        ttk.Separator(side).grid(row=row, column=0, columnspan=3, sticky="ew", pady=12)
        row += 1
        ttk.Label(side, text="Output", style="Section.TLabel").grid(row=row, column=0, columnspan=3, sticky="w", pady=(2, 8))
        row += 1
        row = self._field(side, row, "Aspect", self.aspect_mode, kind="combo", values=("contain", "stretch"))
        row = self._field(side, row, "Min Pitch", self.min_pitch)
        row = self._field(side, row, "Max Pitch", self.max_pitch)
        row = self._field(side, row, "Total Beats", self.total_beats)

        ttk.Separator(side).grid(row=row, column=0, columnspan=3, sticky="ew", pady=12)
        row += 1
        ttk.Label(side, text="Detail", style="Section.TLabel").grid(row=row, column=0, sticky="w")
        ttk.Label(side, textvariable=self.detail_label, style="Value.TLabel").grid(row=row, column=1, columnspan=2, sticky="e")
        row += 1
        ttk.Scale(side, from_=0, to=100, variable=self.detail, command=self._detail_scaled).grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(8, 4),
        )
        row += 1
        ttk.Label(side, textvariable=self.detail_hint, style="PanelMuted.TLabel", wraplength=360).grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0, 8),
        )
        row += 1
        ttk.Checkbutton(side, text="Write edge preview", variable=self.edge_preview_enabled).grid(row=row, column=0, columnspan=3, sticky="w")
        row += 1

        ttk.Separator(side).grid(row=row, column=0, columnspan=3, sticky="ew", pady=12)
        row += 1
        ttk.Label(side, textvariable=self.stats, style="Panel.TLabel", justify="left", wraplength=360).grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        footer = ttk.Frame(outer)
        footer.pack(fill="x", pady=(12, 0))
        ttk.Label(footer, textvariable=self.status, style="Muted.TLabel").pack(side="left")

    def _path_row(self, parent: ttk.Frame, row: int, label: str, variable: StringVar, command) -> int:
        ttk.Label(parent, text=label, style="Panel.TLabel").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", padx=8, pady=4)
        ttk.Button(parent, text="...", width=3, command=command).grid(row=row, column=2, sticky="e", pady=4)
        return row + 1

    def _field(self, parent: ttk.Frame, row: int, label: str, variable, kind: str = "entry", values=()) -> int:
        ttk.Label(parent, text=label, style="Panel.TLabel").grid(row=row, column=0, sticky="w", pady=4)
        if kind == "combo":
            widget = ttk.Combobox(parent, textvariable=variable, values=values, state="readonly")
        else:
            widget = ttk.Entry(parent, textvariable=variable)
        widget.grid(row=row, column=1, columnspan=2, sticky="ew", pady=4)
        return row + 1

    def _detail_scaled(self, _value: str) -> None:
        self._sync_detail_text()

    def _detail_changed(self, *_args) -> None:
        self._sync_detail_text()
        if self._preview_after_id is not None:
            self.root.after_cancel(self._preview_after_id)
        if self.input_path.get() and not self._busy:
            self._preview_after_id = self.root.after(450, self._auto_preview)

    def _auto_preview(self) -> None:
        self._preview_after_id = None
        if self.input_path.get() and not self._busy:
            self.preview_only()

    def _detail_preset(self) -> dict[str, float | int]:
        value = max(0, min(100, self.detail.get())) / 100
        return {
            "note_beats": 0.25 - value * 0.1875,
            "quantize_beats": 0.25 - value * 0.1875,
            "max_width": int(320 + value * 512),
            "canny_low": int(120 - value * 70),
            "canny_high": int(240 - value * 120),
            "min_contour_area": 24.0 - value * 22.0,
            "simplify_epsilon": 3.2 - value * 2.8,
            "sample_step": max(1, int(round(5 - value * 4))),
            "max_notes": int(1400 + value * 9600),
        }

    def _sync_detail_text(self) -> None:
        value = max(0, min(100, self.detail.get()))
        if value < 34:
            name = "Clean"
            hint = "Fewer notes, smoother shapes, calmer MIDI output."
        elif value < 67:
            name = "Balanced"
            hint = "Keeps the image readable while preserving expressive contour detail."
        else:
            name = "Fine"
            hint = "More edge detail and denser MIDI notes for intricate drawings."
        self.detail_label.set(f"{name} {value}%")
        self.detail_hint.set(hint)

    def choose_image(self) -> None:
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("All files", "*.*"),
            ]
        )
        if not path:
            return
        self.input_path.set(path)
        stem = Path(path).stem
        out_dir = Path(path).parent
        self.output_path.set(str(out_dir / f"{stem}.mid"))
        self.preview_path.set(str(out_dir / f"{stem}_preview.png"))
        self.edge_preview_path.set(str(out_dir / f"{stem}_edges.png"))
        self._load_input_preview(Path(path))
        self.status.set("Image loaded.")

    def choose_midi_save(self) -> None:
        self._save_path(self.output_path, ".mid", [("MIDI", "*.mid")])

    def choose_preview_save(self) -> None:
        self._save_path(self.preview_path, ".png", [("PNG", "*.png")])

    def choose_edge_save(self) -> None:
        self._save_path(self.edge_preview_path, ".png", [("PNG", "*.png")])

    def _save_path(self, variable: StringVar, extension: str, filetypes) -> None:
        path = filedialog.asksaveasfilename(defaultextension=extension, filetypes=filetypes)
        if path:
            variable.set(path)

    def preview_only(self) -> None:
        if not self.input_path.get():
            messagebox.showwarning("MidiPainter", "Choose an image first.")
            return
        temp_midi = Path(tempfile.gettempdir()) / "midipainter_preview.mid"
        self._run_conversion(temp_midi, Path(self.preview_path.get()), preview_only=True)

    def convert(self) -> None:
        if not self.input_path.get():
            messagebox.showwarning("MidiPainter", "Choose an image first.")
            return
        self._run_conversion(Path(self.output_path.get()), Path(self.preview_path.get()), preview_only=False)

    def _config(self) -> ConvertConfig:
        detail = self._detail_preset()
        return ConvertConfig(
            min_pitch=self.min_pitch.get(),
            max_pitch=self.max_pitch.get(),
            total_beats=self.total_beats.get(),
            note_beats=float(detail["note_beats"]),
            quantize_beats=float(detail["quantize_beats"]),
            max_width=int(detail["max_width"]),
            canny_low=int(detail["canny_low"]),
            canny_high=int(detail["canny_high"]),
            min_contour_area=float(detail["min_contour_area"]),
            simplify_epsilon=float(detail["simplify_epsilon"]),
            sample_step=int(detail["sample_step"]),
            max_notes=int(detail["max_notes"]),
            aspect_mode=self.aspect_mode.get(),
            auto_sample=True,
        )

    def _run_conversion(self, midi_path: Path, preview_path: Path, preview_only: bool) -> None:
        if self._busy:
            return
        self._busy = True
        self.status.set("Working...")
        edge_path = Path(self.edge_preview_path.get()) if self.edge_preview_enabled.get() else None

        def worker() -> None:
            try:
                result = convert_image_to_midi(
                    Path(self.input_path.get()),
                    midi_path,
                    self._config(),
                    preview_path,
                    edge_path,
                )
            except Exception as exc:
                self.root.after(0, lambda exc=exc: self._finish_error(exc))
                return
            self.root.after(0, lambda result=result: self._finish_success(result, preview_path, preview_only))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_success(self, result: ConvertResult, preview_path: Path, preview_only: bool) -> None:
        self._busy = False
        self._load_roll_preview(preview_path)
        self.stats.set(
            "\n".join(
                [
                    f"Image: {result.image_width}x{result.image_height}",
                    f"Contours: {result.contour_count}/{result.raw_contour_count}",
                    f"Contour points: {result.contour_point_count}",
                    f"Notes: {result.note_count}",
                    f"Aspect: {result.layout.aspect_mode}",
                    f"Layout X: {result.layout.x_offset:.3f} + {result.layout.x_scale:.3f}",
                    f"Layout Y: {result.layout.y_offset:.3f} + {result.layout.y_scale:.3f}",
                ]
            )
        )
        self.status.set("Preview updated." if preview_only else "MIDI exported.")

    def _finish_error(self, exc: Exception) -> None:
        self._busy = False
        self.status.set("Conversion failed.")
        messagebox.showerror("MidiPainter", str(exc))

    def _load_input_preview(self, path: Path) -> None:
        self._input_photo = self._make_photo(path, (460, 520))
        self.input_preview.configure(image=self._input_photo, text="")

    def _load_roll_preview(self, path: Path) -> None:
        self._roll_photo = self._make_photo(path, (560, 520))
        self.roll_preview.configure(image=self._roll_photo, text="")

    def _make_photo(self, path: Path, size: tuple[int, int]) -> ImageTk.PhotoImage:
        image = Image.open(path)
        image.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)


def main() -> int:
    root = Tk()
    MidiPainterApp(root)
    root.mainloop()
    return 0
