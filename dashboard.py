from __future__ import annotations

import customtkinter as ctk

from core import i18n
from core.database import get_palette_count
from core.project_store import list_projects


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, navigate):
        super().__init__(master, fg_color="transparent")
        self.navigate = navigate
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(26, 6))
        ctk.CTkLabel(header, text=i18n.t("home.title"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(header, text=i18n.t("home.subtitle"),
                     text_color=("#85858E", "#8E8E9A")).pack(anchor="w")

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", padx=28, pady=20)

        try:
            projects = len(list_projects())
        except Exception:
            projects = 0
        try:
            palettes = get_palette_count()
        except Exception:
            palettes = 0

        self._card(cards, i18n.t("home.projects"), str(projects),
                   i18n.t("home.open_library"), "library")
        self._card(cards, i18n.t("home.palettes"), str(palettes),
                   i18n.t("home.open_color"), "color_lab")
        self._card(cards, "Editor", "→", i18n.t("home.open_editor"), "editor")

    def _card(self, parent, title, value, action, target):
        card = ctk.CTkFrame(parent, fg_color=("#FFFFFF", "#17171C"), corner_radius=14)
        card.pack(side="left", expand=True, fill="both", padx=8, ipadx=16, ipady=16)
        ctk.CTkLabel(card, text=title, text_color=("#85858E", "#8E8E9A")
                     ).pack(anchor="w", padx=16, pady=(12, 0))
        ctk.CTkLabel(card, text=value,
                     font=ctk.CTkFont(size=30, weight="bold")
                     ).pack(anchor="w", padx=16)
        ctk.CTkButton(card, text=action,
                      command=lambda: self.navigate(target)
                      ).pack(anchor="w", padx=16, pady=(10, 14))