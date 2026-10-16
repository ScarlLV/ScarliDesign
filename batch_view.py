from __future__ import annotations
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageFilter

from core.exporters import save_image
from core.theme import pair


class BatchView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.files: list[Path] = []
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Пакетная обработка", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(self, text="Изображения → одинаковые настройки → папка вывода.",
                     text_color=pair("text_muted")).pack(anchor="w", padx=24)

        bar = ctk.CTkFrame(self, fg_color="transparent"); bar.pack(fill="x", padx=24, pady=14)
        ctk.CTkButton(bar, text="Добавить файлы", command=self._add).pack(side="left")
        ctk.CTkButton(bar, text="Очистить", command=self._clear).pack(side="left", padx=8)

        self.listbox = ctk.CTkTextbox(self, height=200)
        self.listbox.pack(fill="x", padx=24)

        opts = ctk.CTkFrame(self, fg_color=pair("panel"), corner_radius=12)
        opts.pack(fill="x", padx=24, pady=16)
        self._slider(opts, "Яркость", 0.2, 2.0, 1.0, "brightness")
        self._slider(opts, "Контраст", 0.2, 2.0, 1.0, "contrast")
        self._slider(opts, "Насыщенность", 0.0, 2.0, 1.0, "saturation")
        self.resize_enabled = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opts, text="Ресайз по длинной стороне", variable=self.resize_enabled).pack(anchor="w", padx=16, pady=6)
        self.max_side = ctk.CTkEntry(opts, placeholder_text="например, 1600")
        self.max_side.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkButton(self, text="▶ Обработать и сохранить", command=self._run).pack(padx=24, pady=12, fill="x")

    def _slider(self, master, label, frm, to, init, attr):
        row = ctk.CTkFrame(master, fg_color="transparent"); row.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row, text=label, width=120, anchor="w").pack(side="left")
        s = ctk.CTkSlider(row, from_=frm, to=to)
        s.set(init); s.pack(side="left", fill="x", expand=True)
        setattr(self, attr, s)

    def _add(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        for p in paths:
            self.files.append(Path(p))
        self._refresh()

    def _clear(self):
        self.files.clear(); self._refresh()

    def _refresh(self):
        self.listbox.delete("1.0", "end")
        for f in self.files:
            self.listbox.insert("end", str(f) + "\n")

    def _run(self):
        if not self.files:
            messagebox.showwarning("Batch", "Нет файлов"); return
        out_dir = filedialog.askdirectory(title="Папка для результатов")
        if not out_dir:
            return
        out_dir = Path(out_dir)
        try:
            max_side = int(self.max_side.get()) if self.resize_enabled.get() and self.max_side.get() else None
        except ValueError:
            max_side = None
        done = 0
        for f in self.files:
            try:
                img = Image.open(f).convert("RGB")
                img = ImageEnhance.Brightness(img).enhance(float(self.brightness.get()))
                img = ImageEnhance.Contrast(img).enhance(float(self.contrast.get()))
                img = ImageEnhance.Color(img).enhance(float(self.saturation.get()))
                if max_side:
                    img.thumbnail((max_side, max_side))
                save_image(img, out_dir / (f.stem + ".jpg"), fmt="JPG")
                done += 1
            except Exception as exc:
                print("batch error:", f, exc)
        messagebox.showinfo("Batch", f"Готово: {done} / {len(self.files)}")