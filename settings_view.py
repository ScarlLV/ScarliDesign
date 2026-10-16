from __future__ import annotations
import customtkinter as ctk

from core.settings import load_settings, save_settings
from core.theme import pair


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, on_apply):
        super().__init__(master, fg_color="transparent")
        self.on_apply = on_apply
        self.values = load_settings()
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Настройки", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(self, text="Локальный конфиг: ~/.scarlidesign/settings.json",
                     text_color=pair("text_muted")).pack(anchor="w", padx=24)

        box = ctk.CTkFrame(self, fg_color=pair("panel"), corner_radius=12)
        box.pack(fill="x", padx=24, pady=20)

        self.autosave = ctk.IntVar(value=self.values.get("autosave_sec", 60))
        ctk.CTkLabel(box, text="Автосейв, сек", anchor="w").pack(fill="x", padx=16, pady=(14, 0))
        ctk.CTkEntry(box, textvariable=self.autosave).pack(fill="x", padx=16, pady=(0, 8))

        self.grid = ctk.BooleanVar(value=self.values.get("grid", False))
        ctk.CTkCheckBox(box, text="Показывать сетку в редакторе", variable=self.grid).pack(anchor="w", padx=16, pady=4)

        self.dpi = ctk.IntVar(value=self.values.get("export_png_dpi", 144))
        ctk.CTkLabel(box, text="DPI при экспорте PNG", anchor="w").pack(fill="x", padx=16, pady=(10, 0))
        ctk.CTkEntry(box, textvariable=self.dpi).pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkButton(box, text="Сохранить", command=self._save).pack(padx=16, pady=14, fill="x")

    def _save(self):
        self.values["autosave_sec"] = int(self.autosave.get())
        self.values["grid"] = bool(self.grid.get())
        self.values["export_png_dpi"] = int(self.dpi.get())
        save_settings(self.values)
        if self.on_apply:
            self.on_apply()