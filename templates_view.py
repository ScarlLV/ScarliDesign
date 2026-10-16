from __future__ import annotations
import customtkinter as ctk

from core import templates
from core.theme import pair


class TemplatesView(ctk.CTkFrame):
    def __init__(self, master, on_pick):
        super().__init__(master, fg_color="transparent")
        self.on_pick = on_pick
        ctk.CTkLabel(self, text="Шаблоны", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(self, text="Готовые композиции — один клик, и редактор заполнен.",
                     text_color=pair("text_muted")).pack(anchor="w", padx=24)

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=24, pady=20)
        for i, name in enumerate(templates.names()):
            card = ctk.CTkFrame(grid, fg_color=pair("panel"), corner_radius=12)
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=8, pady=8)
            grid.grid_columnconfigure(i % 3, weight=1)
            ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=(14, 2))
            t = templates.get(name)
            size = t.get("size", ("—", "—"))
            ctk.CTkLabel(card, text=f"{size[0]} × {size[1]}", text_color=pair("text_muted")).pack(anchor="w", padx=16)
            ctk.CTkButton(card, text="Открыть", command=lambda n=name: self._pick(n)).pack(padx=16, pady=14, fill="x")

    def _pick(self, name: str):
        self.on_pick(name)