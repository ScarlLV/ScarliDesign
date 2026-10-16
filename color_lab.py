from __future__ import annotations

import colorsys
import json
import random
from tkinter import colorchooser, filedialog, messagebox

import customtkinter as ctk

from core import i18n
from core.database import save_palette, get_palettes, delete_palette


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def _hls_shift(hexv, dh=0.0, dl=0.0, ds=0.0):
    r, g, b = _hex_to_rgb(hexv)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    h = (h + dh) % 1.0
    l = max(0.0, min(1.0, l + dl))
    s = max(0.0, min(1.0, s + ds))
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return _rgb_to_hex((r2 * 255, g2 * 255, b2 * 255))


SCHEMES = {
    "cl.scheme.analogous": lambda c: [c, _hls_shift(c, 0.05), _hls_shift(c, -0.05),
                                       _hls_shift(c, 0.10), _hls_shift(c, -0.10)],
    "cl.scheme.complementary": lambda c: [c, _hls_shift(c, 0.5)],
    "cl.scheme.triadic": lambda c: [c, _hls_shift(c, 1 / 3), _hls_shift(c, 2 / 3)],
    "cl.scheme.split": lambda c: [c, _hls_shift(c, 5 / 12), _hls_shift(c, 7 / 12)],
    "cl.scheme.tetradic": lambda c: [c, _hls_shift(c, 0.25),
                                      _hls_shift(c, 0.5), _hls_shift(c, 0.75)],
    "cl.scheme.mono": lambda c: [_hls_shift(c, 0, dl=d) for d in
                                  (-0.3, -0.15, 0.0, 0.15, 0.3)],
    "cl.scheme.random": lambda c: ["#%02x%02x%02x" %
                                    tuple(random.randint(0, 255) for _ in range(3))
                                    for _ in range(5)],
}


class ColorLabView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.base = "#8A7BD8"
        self.colors: list[str] = []
        self._build()
        self.generate()

    def _build(self):
        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=28, pady=(26, 4))
        ctk.CTkLabel(head, text=i18n.t("cl.title"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(head, text=i18n.t("cl.subtitle"),
                     text_color=("#85858E", "#8E8E9A")).pack(anchor="w")

        ctrl = ctk.CTkFrame(self, fg_color="transparent")
        ctrl.pack(fill="x", padx=28, pady=14)

        ctk.CTkButton(ctrl, text=i18n.t("cl.base"),
                      command=self.pick_base).pack(side="left", padx=(0, 8))

        self.scheme_display = {key: i18n.t(key) for key in SCHEMES.keys()}
        self.scheme_var = ctk.StringVar(value=i18n.t("cl.scheme.analogous"))
        ctk.CTkOptionMenu(ctrl, values=list(self.scheme_display.values()),
                          variable=self.scheme_var,
                          command=lambda _v: self.generate()).pack(side="left", padx=8)

        ctk.CTkButton(ctrl, text=i18n.t("cl.generate"),
                      command=self.generate).pack(side="left", padx=8)
        ctk.CTkButton(ctrl, text=i18n.t("cl.copy_all"),
                      command=self.copy_all).pack(side="left", padx=8)
        ctk.CTkButton(ctrl, text=i18n.t("cl.save"),
                      command=self.save_current).pack(side="left", padx=8)
        ctk.CTkButton(ctrl, text=i18n.t("cl.export_json"),
                      command=self.export_json).pack(side="left", padx=8)
        ctk.CTkButton(ctrl, text=i18n.t("cl.export_css"),
                      command=self.export_css).pack(side="left", padx=8)

        self.rows = ctk.CTkFrame(self, fg_color="transparent")
        self.rows.pack(fill="both", expand=True, padx=28, pady=(10, 0))

        # сохранённые палитры
        ctk.CTkLabel(self, text=i18n.t("lib.palettes"),
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).pack(anchor="w", padx=28, pady=(14, 4))
        self.saved = ctk.CTkScrollableFrame(self, height=160,
                                             fg_color=("#FFFFFF", "#17171C"))
        self.saved.pack(fill="x", expand=False, padx=28, pady=(0, 20))
        self._refresh_saved()

    def _scheme_key(self) -> str:
        label = self.scheme_var.get()
        for k, v in self.scheme_display.items():
            if v == label:
                return k
        return "cl.scheme.analogous"

    def pick_base(self):
        _rgb, hexv = colorchooser.askcolor(color=self.base)
        if hexv:
            self.base = hexv
            self.generate()

    def generate(self):
        key = self._scheme_key()
        self.colors = SCHEMES[key](self.base)
        self._render_rows()

    def _render_rows(self):
        for w in self.rows.winfo_children():
            w.destroy()
        for c in self.colors:
            row = ctk.CTkFrame(self.rows, fg_color=("#FFFFFF", "#17171C"),
                               corner_radius=10)
            row.pack(fill="x", pady=4)
            sw = ctk.CTkFrame(row, width=60, height=40, fg_color=c,
                              corner_radius=8)
            sw.pack(side="left", padx=10, pady=10)
            sw.pack_propagate(False)
            ctk.CTkLabel(row, text=c,
                         font=ctk.CTkFont(size=13, family="Consolas")
                         ).pack(side="left", padx=8)
            ctk.CTkButton(row, text=i18n.t("cl.copy_hex"), width=110,
                          command=lambda col=c: self.copy_hex(col)
                          ).pack(side="right", padx=10)

    def _refresh_saved(self):
        for w in self.saved.winfo_children():
            w.destroy()
        try:
            items = get_palettes()
        except Exception:
            items = []
        if not items:
            ctk.CTkLabel(self.saved, text=i18n.t("lib.empty"),
                         text_color=("#85858E", "#8E8E9A")).pack(pady=10)
            return
        for entry in items:
            pid = entry["id"]
            name = entry["name"]
            colors = entry["colors"]
            row = ctk.CTkFrame(self.saved, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=name, width=140, anchor="w"
                         ).pack(side="left", padx=6)
            swatch = ctk.CTkFrame(row, fg_color="transparent")
            swatch.pack(side="left", padx=4)
            for c in (colors or [])[:8]:
                s = ctk.CTkFrame(swatch, width=18, height=18, fg_color=c,
                                 corner_radius=4)
                s.pack(side="left", padx=1)
                s.pack_propagate(False)
            ctk.CTkButton(row, text=i18n.t("lib.copy"), width=90,
                          command=lambda c=colors: self._copy_list(c)
                          ).pack(side="right", padx=4)
            ctk.CTkButton(row, text=i18n.t("lib.delete"), width=80,
                          fg_color="#7B2D2D", hover_color="#9A3939",
                          command=lambda i=pid: self._delete(i)
                          ).pack(side="right", padx=4)

    def _delete(self, pid):
        if not messagebox.askyesno(i18n.t("lib.title"),
                                    i18n.t("lib.confirm_delete")):
            return
        try:
            delete_palette(pid)
        except Exception as exc:
            messagebox.showerror(i18n.t("lib.title"), str(exc))
        self._refresh_saved()

    def copy_hex(self, value: str):
        self.clipboard_clear()
        self.clipboard_append(value)

    def _copy_list(self, colors):
        self.clipboard_clear()
        self.clipboard_append(", ".join(colors or []))

    def copy_all(self):
        self.clipboard_clear()
        self.clipboard_append(", ".join(self.colors))

    def save_current(self):
        if not self.colors:
            return
        name = self.scheme_var.get() or "Palette"
        try:
            save_palette(name, self.colors)
            messagebox.showinfo(i18n.t("cl.title"), i18n.t("cl.saved"))
            self._refresh_saved()
        except Exception as exc:
            messagebox.showerror(i18n.t("cl.title"), str(exc))

    def export_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"colors": self.colors}, f, indent=2)
        except Exception as exc:
            messagebox.showerror(i18n.t("cl.title"), str(exc))

    def export_css(self):
        path = filedialog.asksaveasfilename(defaultextension=".css",
                                            filetypes=[("CSS", "*.css")])
        if not path:
            return
        try:
            lines = [":root {"]
            for i, c in enumerate(self.colors, 1):
                lines.append(f"  --color-{i}: {c};")
            lines.append("}")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception as exc:
            messagebox.showerror(i18n.t("cl.title"), str(exc))