from __future__ import annotations

from tkinter import messagebox

import customtkinter as ctk

from core import i18n
from core.project_store import list_projects, delete_project
from core.database import get_palettes, delete_palette


class ProjectsView(ctk.CTkFrame):
    def __init__(self, master, navigate):
        super().__init__(master, fg_color="transparent")
        self.navigate = navigate
        self._build()

    def _build(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=28, pady=(26, 4))
        ctk.CTkLabel(head, text=i18n.t("lib.title"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(head, text=i18n.t("lib.subtitle"),
                     text_color=("#85858E", "#8E8E9A")).pack(anchor="w")

        tabs = ctk.CTkTabview(self, fg_color=("#FFFFFF", "#17171C"))
        tabs.pack(fill="both", expand=True, padx=28, pady=18)

        tab_p = tabs.add(i18n.t("lib.projects"))
        tab_l = tabs.add(i18n.t("lib.palettes"))

        self._fill_projects(tab_p)
        self._fill_palettes(tab_l)

    def _fill_projects(self, parent):
        try:
            items = list_projects()
        except Exception:
            items = []
        if not items:
            ctk.CTkLabel(parent, text=i18n.t("lib.empty"),
                         text_color=("#85858E", "#8E8E9A")).pack(pady=20)
            return
        for item in items:
            # list_projects может вернуть str или dict — поддержим оба
            if isinstance(item, str):
                path = item
                name = path.split("/")[-1].split("\\")[-1]
            else:
                path = item.get("path", "")
                name = item.get("name") or path.split("/")[-1].split("\\")[-1]

            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=name, anchor="w").pack(side="left", padx=8)
            ctk.CTkButton(row, text=i18n.t("lib.open"), width=90,
                          command=lambda p=path: self.navigate("editor", p)
                          ).pack(side="right", padx=4)
            ctk.CTkButton(row, text=i18n.t("lib.delete"), width=90,
                          fg_color="#7B2D2D", hover_color="#9A3939",
                          command=lambda p=path: self._del_project(p)
                          ).pack(side="right", padx=4)

    def _fill_palettes(self, parent):
        try:
            items = get_palettes()
        except Exception:
            items = []
        if not items:
            ctk.CTkLabel(parent, text=i18n.t("lib.empty"),
                         text_color=("#85858E", "#8E8E9A")).pack(pady=20)
            return
        for entry in items:
            pid = entry["id"]
            name = entry["name"]
            colors = entry["colors"]
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=name, width=180, anchor="w"
                         ).pack(side="left", padx=8)
            swatch = ctk.CTkFrame(row, fg_color="transparent")
            swatch.pack(side="left", padx=6)
            for c in (colors or [])[:8]:
                s = ctk.CTkFrame(swatch, width=18, height=18, fg_color=c,
                                 corner_radius=4)
                s.pack(side="left", padx=1)
                s.pack_propagate(False)
            ctk.CTkButton(row, text=i18n.t("lib.copy"), width=100,
                          command=lambda c=colors: self._copy(", ".join(c or []))
                          ).pack(side="right", padx=4)
            ctk.CTkButton(row, text=i18n.t("lib.delete"), width=90,
                          fg_color="#7B2D2D", hover_color="#9A3939",
                          command=lambda i=pid: self._del_palette(i)
                          ).pack(side="right", padx=4)

    def _copy(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)

    def _del_project(self, path):
        if not messagebox.askyesno(i18n.t("lib.title"),
                                    i18n.t("lib.confirm_delete")):
            return
        try:
            delete_project(path)
        except Exception as exc:
            messagebox.showerror(i18n.t("lib.title"), str(exc))
        self.refresh()

    def _del_palette(self, pid):
        if not messagebox.askyesno(i18n.t("lib.title"),
                                    i18n.t("lib.confirm_delete")):
            return
        try:
            delete_palette(pid)
        except Exception as exc:
            messagebox.showerror(i18n.t("lib.title"), str(exc))
        self.refresh()

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()