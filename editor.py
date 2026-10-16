from __future__ import annotations

import json
import random
from pathlib import Path
from tkinter import Canvas, filedialog, colorchooser, messagebox

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter

from core import i18n
from core.palettes import PALETTES


CANVAS_PRESETS = {
    "Square 1080":     (1080, 1080),
    "Cover 3000":      (3000, 3000),
    "Poster A4":       (2480, 3508),
    "Story 9:16":      (1080, 1920),
    "YouTube 16:9":    (1280, 720),
    "Banner 1920×600": (1920, 600),
}


class EditorView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.size = (1080, 1080)
        self.bg_mode = "solid"
        self.bg_color = "#0E0E12"
        self.bg_color2 = "#5C4BA5"
        self.bg_image: Image.Image | None = None
        self.bg_image_path: str | None = None
        self.bg_dim = 0.35
        self.grain = 0.0
        self.vignette = 0.0
        self.align = "left"
        self.title = "ScarliDesign"
        self.subtitle = "creative workspace"
        self.caption = ""
        self.title_size = 96
        self.subtitle_size = 34
        self.caption_size = 22
        self.title_y = 0.42
        self.line_spacing = 1.15
        self.tracking = 0
        self.uppercase = False
        self.text_color = "#F5F5F7"
        self.accent = "bar"
        self.accent_color = "#8A7BD8"
        self.shadow = 0
        self.outline = 0
        self.safe_area = False

        self.recent_colors: list[str] = []

        self._render_job = None
        self._photo = None
        self._eyedropper_active = False
        self._binds: list = []

        self._build_sidebar()
        self._build_canvas()
        self._bind_keys()
        self.after(60, self._schedule_render)

    # ============================================================
    # UI
    # ============================================================
    def _build_sidebar(self):
        self.side = ctk.CTkScrollableFrame(self, width=310,
                                            fg_color=("#FFFFFF", "#17171C"))
        self.side.grid(row=0, column=0, sticky="nsw", padx=(0, 1))

        ctk.CTkLabel(self.side, text=i18n.t("editor.header"),
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=("#85858E", "#8E8E9A")
                     ).pack(anchor="w", padx=14, pady=(14, 6))

        self._label("editor.canvas")
        self.size_var = ctk.StringVar(value="Square 1080")
        ctk.CTkOptionMenu(self.side, values=list(CANVAS_PRESETS.keys()),
                          variable=self.size_var,
                          command=self._apply_size).pack(fill="x", padx=14)

        self._label("editor.palettes")
        self.palette_var = ctk.StringVar(value="—")
        ctk.CTkOptionMenu(self.side, values=["—"] + list(PALETTES.keys()),
                          variable=self.palette_var,
                          command=self._apply_palette).pack(fill="x", padx=14)

        self._label("editor.recent")
        self.recent_bar = ctk.CTkFrame(self.side, fg_color="transparent")
        self.recent_bar.pack(fill="x", padx=14, pady=(0, 6))

        self._label("editor.background")
        self.bg_mode_var = ctk.StringVar(value=self.bg_mode)
        ctk.CTkSegmentedButton(
            self.side,
            values=["solid", "gradient", "image", "duotone"],
            variable=self.bg_mode_var,
            command=self._set_bg_mode,
        ).pack(fill="x", padx=14)

        row = ctk.CTkFrame(self.side, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=6)
        ctk.CTkButton(row, text=i18n.t("editor.color1"),
                      command=lambda: self._pick_color("bg_color")
                      ).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ctk.CTkButton(row, text=i18n.t("editor.color2"),
                      command=lambda: self._pick_color("bg_color2")
                      ).pack(side="left", expand=True, fill="x", padx=(3, 0))

        ctk.CTkButton(self.side, text=i18n.t("editor.load_image"),
                      command=self._pick_bg_image
                      ).pack(fill="x", padx=14, pady=(0, 4))

        self._slider("editor.dim", 0.0, 1.0, self.bg_dim,
                     lambda v: self._set("bg_dim", float(v)))
        self._slider("editor.vignette", 0.0, 1.0, self.vignette,
                     lambda v: self._set("vignette", float(v)))

        self._label("editor.title")
        self.title_box = ctk.CTkTextbox(self.side, height=70)
        self.title_box.pack(fill="x", padx=14)
        self.title_box.insert("1.0", self.title)
        self.title_box.bind("<KeyRelease>", self._on_title_change)

        self._label("editor.subtitle")
        self.sub_box = ctk.CTkEntry(self.side)
        self.sub_box.pack(fill="x", padx=14)
        self.sub_box.insert(0, self.subtitle)
        self.sub_box.bind("<KeyRelease>",
                          lambda e: self._set("subtitle", self.sub_box.get()))

        self._label("editor.caption")
        self.cap_box = ctk.CTkEntry(self.side)
        self.cap_box.pack(fill="x", padx=14)
        self.cap_box.insert(0, self.caption)
        self.cap_box.bind("<KeyRelease>",
                          lambda e: self._set("caption", self.cap_box.get()))

        self._label("editor.align")
        row = ctk.CTkFrame(self.side, fg_color="transparent")
        row.pack(fill="x", padx=14)
        for label, val in (("◧", "left"), ("▣", "center"), ("◨", "right")):
            ctk.CTkButton(row, text=label, width=40,
                          command=lambda v=val: self._set("align", v)
                          ).pack(side="left", padx=2)

        self._slider("editor.title_size", 20, 400, self.title_size,
                     lambda v: self._set("title_size", int(float(v))))
        self._slider("editor.subtitle_size", 12, 160, self.subtitle_size,
                     lambda v: self._set("subtitle_size", int(float(v))))
        self._slider("editor.caption_size", 8, 80, self.caption_size,
                     lambda v: self._set("caption_size", int(float(v))))
        self._slider("editor.title_y", 0.0, 1.0, self.title_y,
                     lambda v: self._set("title_y", float(v)))
        self._slider("editor.line_height", 0.8, 2.0, self.line_spacing,
                     lambda v: self._set("line_spacing", float(v)))
        self._slider("editor.tracking", -10, 40, self.tracking,
                     lambda v: self._set("tracking", int(float(v))))

        self.upper_var = ctk.BooleanVar(value=self.uppercase)
        ctk.CTkCheckBox(self.side, text=i18n.t("editor.uppercase"),
                        variable=self.upper_var,
                        command=lambda: self._set("uppercase",
                                                   bool(self.upper_var.get()))
                        ).pack(anchor="w", padx=14, pady=(6, 0))

        row = ctk.CTkFrame(self.side, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(10, 0))
        ctk.CTkButton(row, text=i18n.t("editor.text_color"),
                      command=lambda: self._pick_color("text_color")
                      ).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ctk.CTkButton(row, text=i18n.t("editor.accent_color"),
                      command=lambda: self._pick_color("accent_color")
                      ).pack(side="left", expand=True, fill="x", padx=(3, 0))

        ctk.CTkButton(self.side, text=i18n.t("editor.eyedropper"),
                      command=self._start_eyedropper
                      ).pack(fill="x", padx=14, pady=(6, 0))

        self._label("editor.accent")
        self.accent_var = ctk.StringVar(value=self.accent)
        ctk.CTkSegmentedButton(
            self.side, values=["none", "bar", "circle", "frame"],
            variable=self.accent_var,
            command=lambda _v: self._set("accent", self.accent_var.get()),
        ).pack(fill="x", padx=14)

        self._slider("editor.shadow", 0, 20, self.shadow,
                     lambda v: self._set("shadow", int(float(v))))
        self._slider("editor.outline", 0, 10, self.outline,
                     lambda v: self._set("outline", int(float(v))))

        self.safe_var = ctk.BooleanVar(value=self.safe_area)
        ctk.CTkCheckBox(self.side, text=i18n.t("editor.safe_area"),
                        variable=self.safe_var,
                        command=lambda: self._set("safe_area",
                                                   bool(self.safe_var.get()))
                        ).pack(anchor="w", padx=14, pady=(6, 0))

        ctk.CTkButton(self.side, text=i18n.t("editor.random"),
                      command=self.randomize
                      ).pack(fill="x", padx=14, pady=(14, 4))
        ctk.CTkButton(self.side, text=i18n.t("editor.export_png"),
                      command=lambda: self.export("PNG")
                      ).pack(fill="x", padx=14, pady=(0, 4))
        ctk.CTkButton(self.side, text=i18n.t("editor.export_jpg"),
                      command=lambda: self.export("JPG")
                      ).pack(fill="x", padx=14, pady=(0, 4))
        ctk.CTkButton(self.side, text=i18n.t("editor.save_project"),
                      command=self.save_project
                      ).pack(fill="x", padx=14, pady=(0, 4))
        ctk.CTkButton(self.side, text=i18n.t("editor.open_project"),
                      command=self.open_project
                      ).pack(fill="x", padx=14, pady=(0, 16))

        self.status = ctk.CTkLabel(self.side, text=i18n.t("editor.status.ready"),
                                    text_color=("#85858E", "#8E8E9A"),
                                    font=ctk.CTkFont(size=10))
        self.status.pack(anchor="w", padx=14, pady=(0, 10))

        self._refresh_recent()

    def _label(self, key: str):
        ctk.CTkLabel(self.side, text=i18n.t(key)).pack(
            anchor="w", padx=14, pady=(10, 2))

    def _slider(self, key: str, frm, to, init, cmd):
        ctk.CTkLabel(self.side, text=i18n.t(key)).pack(
            anchor="w", padx=14, pady=(8, 0))
        s = ctk.CTkSlider(self.side, from_=frm, to=to, command=cmd)
        s.set(init)
        s.pack(fill="x", padx=14)

    def _build_canvas(self):
        wrap = ctk.CTkFrame(self, fg_color=("#EAEAEE", "#0B0B0E"))
        wrap.grid(row=0, column=1, sticky="nsew")
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(wrap, background="#0B0B0E", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda e: self._schedule_render())
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    def _bind_keys(self):
        # CTkFrame запрещает bind_all — используем корневое окно
        root = self.winfo_toplevel()
        self._binds = [
            root.bind("<Control-e>", lambda e: self.export("PNG"), add="+"),
            root.bind("<Control-s>", lambda e: self.save_project(), add="+"),
            root.bind("<Control-r>", lambda e: self.randomize(), add="+"),
            root.bind("<Control-i>", lambda e: self._swap_colors(), add="+"),
        ]

    def destroy(self):
        # снимаем хоткеи, чтобы не накапливались при переключении вкладок
        try:
            root = self.winfo_toplevel()
            for seq, funcid in getattr(self, "_binds", []):
                try:
                    root.unbind(seq, funcid)
                except Exception:
                    pass
        except Exception:
            pass
        super().destroy()

    # ============================================================
    # state
    # ============================================================
    def _on_title_change(self, _e=None):
        self.title = self.title_box.get("1.0", "end").rstrip("\n")
        self._schedule_render()

    def _set(self, name, value):
        setattr(self, name, value)
        self._schedule_render()

    def _swap_colors(self):
        self.bg_color, self.text_color = self.text_color, self.bg_color
        self._schedule_render()

    def _apply_size(self, name):
        if name in CANVAS_PRESETS:
            self.size = CANVAS_PRESETS[name]
            self._schedule_render()

    def _set_bg_mode(self, mode):
        self.bg_mode = mode
        self._schedule_render()

    def _apply_palette(self, name):
        colors = PALETTES.get(name)
        if not colors:
            return
        self.bg_color = colors[0]
        self.text_color = colors[-1]
        self.accent_color = colors[1] if len(colors) > 1 else colors[0]
        self._remember(colors)
        self._schedule_render()

    def _pick_color(self, attr):
        current = getattr(self, attr, "#ffffff")
        _rgb, hexv = colorchooser.askcolor(color=current)
        if hexv:
            setattr(self, attr, hexv)
            self._remember([hexv])
            self._schedule_render()

    def _remember(self, colors):
        for c in colors:
            if c not in self.recent_colors:
                self.recent_colors.append(c)
        self.recent_colors = self.recent_colors[-12:]
        self._refresh_recent()

    def _refresh_recent(self):
        if not hasattr(self, "recent_bar"):
            return
        for w in self.recent_bar.winfo_children():
            w.destroy()
        for c in self.recent_colors[-8:]:
            btn = ctk.CTkButton(self.recent_bar, text="", width=22, height=22,
                                fg_color=c, hover_color=c,
                                command=lambda col=c: self._use_recent(col))
            btn.pack(side="left", padx=2)

    def _use_recent(self, color):
        self.text_color = color
        self._schedule_render()

    def _pick_bg_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if not path:
            return
        try:
            self.bg_image = Image.open(path).convert("RGB")
            self.bg_image_path = path
            self.bg_mode = "image"
            self.bg_mode_var.set("image")
            self._schedule_render()
        except Exception as exc:
            messagebox.showerror(i18n.t("dlg.image"), str(exc))

    def randomize(self):
        r = lambda: "#%02x%02x%02x" % tuple(random.randint(0, 255)
                                             for _ in range(3))
        self.bg_color = r()
        self.bg_color2 = r()
        self.accent_color = r()
        self.text_color = "#F5F5F7" if _luma(self.bg_color) < 0.5 else "#111114"
        self.accent = random.choice(["bar", "circle", "frame", "none"])
        self.align = random.choice(["left", "center", "right"])
        self.bg_mode = random.choice(["solid", "gradient", "duotone"])
        self.bg_mode_var.set(self.bg_mode)
        self.accent_var.set(self.accent)
        self._schedule_render()

    # ============================================================
    # eyedropper
    # ============================================================
    def _start_eyedropper(self):
        self._eyedropper_active = True
        try:
            self.canvas.configure(cursor="crosshair")
        except Exception:
            pass

    def _on_canvas_click(self, event):
        if not self._eyedropper_active:
            return
        self._eyedropper_active = False
        try:
            self.canvas.configure(cursor="")
        except Exception:
            pass
        if self._photo is None:
            return
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        W, H = self._photo.width(), self._photo.height()
        ox, oy = (cw - W) // 2, (ch - H) // 2
        x = int(event.x - ox)
        y = int(event.y - oy)
        if x < 0 or y < 0 or x >= W or y >= H:
            return
        try:
            rgb = self._photo.get(x, y)
        except Exception:
            return
        hexv = "#%02x%02x%02x" % rgb[:3]
        self.text_color = hexv
        self._remember([hexv])
        self._schedule_render()

    # ============================================================
    # render
    # ============================================================
    def _schedule_render(self):
        if self._render_job:
            try:
                self.after_cancel(self._render_job)
            except Exception:
                pass
        self._render_job = self.after(80, self._render_preview)

    def _render_preview(self):
        self._render_job = None
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 20 or ch < 20:
            self._render_job = self.after(80, self._render_preview)
            return

        W, H = self.size
        scale = min((cw - 40) / W, (ch - 40) / H, 1.0)
        if scale <= 0:
            return
        pw, ph = max(1, int(W * scale)), max(1, int(H * scale))

        try:
            img = self._render_image(pw, ph)
        except Exception as exc:
            print("render error:", exc)
            return

        self._photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        ox, oy = (cw - pw) // 2, (ch - ph) // 2
        self.canvas.create_image(ox, oy, anchor="nw", image=self._photo)
        self.canvas.create_rectangle(ox, oy, ox + pw, oy + ph,
                                     outline="#555", width=1)

        if self.safe_area:
            m = int(min(pw, ph) * 0.05)
            self.canvas.create_rectangle(ox + m, oy + m,
                                          ox + pw - m, oy + ph - m,
                                          outline="#FF5C8A", width=1,
                                          dash=(4, 4))
        try:
            self.status.configure(text=i18n.t("editor.status.ready"))
        except Exception:
            pass

    def _render_image(self, W: int, H: int) -> Image.Image:
        bg = self._render_background(W, H)
        draw = ImageDraw.Draw(bg)

        accent = _hex(self.accent_color)
        if self.accent == "bar":
            x0 = int(W * 0.08)
            y0 = int(H * self.title_y) - int(H * 0.045)
            x1 = x0 + max(3, int(W * 0.006))
            y1 = int(H * self.title_y) + int(H * 0.06)
            draw.rectangle([x0, y0, x1, y1], fill=accent)
        elif self.accent == "circle":
            r = int(min(W, H) * 0.09)
            cx, cy = int(W * 0.12), int(H * 0.16)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
        elif self.accent == "frame":
            m = int(min(W, H) * 0.04)
            draw.rectangle([m, m, W - m, H - m], outline=accent,
                           width=max(2, int(min(W, H) * 0.003)))

        title_font = _font(int(self.title_size))
        sub_font = _font(int(self.subtitle_size))
        cap_font = _font(int(self.caption_size))

        pad = int(W * 0.07)
        raw_title = self.title.upper() if self.uppercase else self.title
        lines = raw_title.split("\n") if raw_title else []
        line_h = int(self.title_size * self.line_spacing)
        y = int(H * self.title_y)

        for i, line in enumerate(lines):
            _draw_styled(draw, line, self.align, W, pad, y + i * line_h,
                         title_font, self.text_color, self.tracking,
                         self.shadow, self.outline)

        y_after = y + len(lines) * line_h + int(self.title_size * 0.1)
        if self.subtitle:
            sub = self.subtitle.upper() if self.uppercase else self.subtitle
            _draw_styled(draw, sub, self.align, W, pad, y_after, sub_font,
                         self.text_color, 0, self.shadow, self.outline)
        if self.caption:
            cap = self.caption.upper() if self.uppercase else self.caption
            _draw_styled(draw, cap, self.align, W, pad, H - int(H * 0.06),
                         cap_font, self.text_color, 0, self.shadow, self.outline)

        if self.vignette > 0:
            bg = _apply_vignette(bg, self.vignette)
        return bg

    def _render_background(self, W: int, H: int) -> Image.Image:
        if self.bg_mode == "image" and self.bg_image is not None:
            base = self.bg_image.copy()
            base.thumbnail((W, H))
            bg = Image.new("RGB", (W, H), (0, 0, 0))
            bg.paste(base, ((W - base.width) // 2, (H - base.height) // 2))
            if self.bg_dim > 0:
                bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)),
                                 self.bg_dim)
        elif self.bg_mode == "gradient":
            bg = _gradient(W, H, self.bg_color, self.bg_color2)
        elif self.bg_mode == "duotone":
            bg = _duotone(W, H, self.bg_color, self.bg_color2)
        else:
            bg = Image.new("RGB", (W, H), _hex(self.bg_color))
        return bg

    # ============================================================
    # export / project
    # ============================================================
    def export(self, fmt):
        ext = ".png" if fmt == "PNG" else ".jpg"
        path = filedialog.asksaveasfilename(
            defaultextension=ext, filetypes=[(fmt, f"*{ext}")]
        )
        if not path:
            return
        try:
            img = self._render_image(*self.size)
            if fmt == "JPG" and img.mode != "RGB":
                img = img.convert("RGB")
            img.save(path, format=fmt, quality=95 if fmt == "JPG" else None)
            messagebox.showinfo(i18n.t("dlg.export"),
                                i18n.t("dlg.export_saved", path=path))
        except Exception as exc:
            messagebox.showerror(i18n.t("dlg.export"), str(exc))

    def _snapshot(self) -> dict:
        return {
            "size": self.size, "bg_mode": self.bg_mode,
            "bg_color": self.bg_color, "bg_color2": self.bg_color2,
            "bg_image_path": self.bg_image_path, "bg_dim": self.bg_dim,
            "grain": self.grain, "vignette": self.vignette,
            "align": self.align, "title": self.title,
            "subtitle": self.subtitle, "caption": self.caption,
            "title_size": self.title_size, "subtitle_size": self.subtitle_size,
            "caption_size": self.caption_size, "title_y": self.title_y,
            "line_spacing": self.line_spacing, "tracking": self.tracking,
            "uppercase": self.uppercase,
            "text_color": self.text_color,
            "accent": self.accent, "accent_color": self.accent_color,
            "shadow": self.shadow, "outline": self.outline,
            "safe_area": self.safe_area,
        }

    def save_project(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".scarli", filetypes=[("Scarli", "*.scarli")]
        )
        if not path:
            return
        try:
            Path(path).write_text(
                json.dumps(self._snapshot(), indent=2, ensure_ascii=False),
                encoding="utf-8")
            messagebox.showinfo(i18n.t("dlg.project"),
                                i18n.t("dlg.project_saved"))
        except Exception as exc:
            messagebox.showerror(i18n.t("dlg.project"), str(exc))

    def open_project(self):
        path = filedialog.askopenfilename(filetypes=[("Scarli", "*.scarli")])
        if path:
            self.load_project_file(path)

    def load_project_file(self, path):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as exc:
            messagebox.showerror(i18n.t("dlg.project"), str(exc))
            return
        if "size" in data:
            data["size"] = tuple(data["size"])
        for k, v in data.items():
            setattr(self, k, v)

        self.title_box.delete("1.0", "end")
        self.title_box.insert("1.0", self.title)
        self.sub_box.delete(0, "end")
        self.sub_box.insert(0, self.subtitle)
        self.cap_box.delete(0, "end")
        self.cap_box.insert(0, self.caption)
        self.bg_mode_var.set(self.bg_mode)
        self.accent_var.set(self.accent)

        if self.bg_image_path:
            try:
                self.bg_image = Image.open(self.bg_image_path).convert("RGB")
            except Exception:
                self.bg_image = None
        self._schedule_render()


# ============================================================
# helpers
# ============================================================
def _hex(c: str):
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _luma(hexv: str) -> float:
    r, g, b = _hex(hexv)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


_FONT_CACHE: dict[int, ImageFont.ImageFont] = {}


def _font(size: int):
    size = max(8, int(size))
    if size in _FONT_CACHE:
        return _FONT_CACHE[size]
    for name in ("DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf",
                 "Helvetica-Bold.ttf", "DejaVuSans.ttf"):
        try:
            f = ImageFont.truetype(name, size)
            _FONT_CACHE[size] = f
            return f
        except Exception:
            continue
    f = ImageFont.load_default()
    _FONT_CACHE[size] = f
    return f


def _gradient(W, H, c1, c2):
    a, b = _hex(c1), _hex(c2)
    col = Image.new("RGB", (1, H))
    px = col.load()
    for y in range(H):
        t = y / max(1, H - 1)
        px[0, y] = (int(a[0] * (1 - t) + b[0] * t),
                    int(a[1] * (1 - t) + b[1] * t),
                    int(a[2] * (1 - t) + b[2] * t))
    return col.resize((W, H), Image.NEAREST)


def _duotone(W, H, dark, light):
    grad = _gradient(W, H, dark, light)
    return grad.rotate(45, expand=False).crop((0, 0, W, H))


def _draw_styled(draw, text, align, W, pad, y, font, color,
                 tracking=0, shadow=0, outline=0):
    if not text:
        return
    tw = 0
    for ch in text:
        bbox = _bbox(draw, ch, font)
        tw += bbox[2] - bbox[0] + tracking
    tw = max(0, tw - tracking)

    if align == "center":
        x = (W - tw) // 2
    elif align == "right":
        x = W - pad - tw
    else:
        x = pad

    cx = x
    for ch in text:
        if shadow > 0:
            draw.text((cx + shadow, y + shadow), ch, font=font, fill=(0, 0, 0))
        if outline > 0:
            for dx in (-outline, 0, outline):
                for dy in (-outline, 0, outline):
                    if dx or dy:
                        draw.text((cx + dx, y + dy), ch, font=font, fill=color)
        draw.text((cx, y), ch, font=font, fill=color)
        bbox = _bbox(draw, ch, font)
        cx += (bbox[2] - bbox[0]) + tracking


def _bbox(draw, text, font):
    try:
        return draw.textbbox((0, 0), text, font=font)
    except Exception:
        w, h = draw.textsize(text, font=font)
        return (0, 0, w, h)


def _apply_vignette(img: Image.Image, amount: float) -> Image.Image:
    W, H = img.size
    mask = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(mask)
    m = int(min(W, H) * 0.1)
    draw.ellipse([-m, -m, W + m, H + m], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(W, H) * 0.15))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    v = Image.composite(img, dark, mask)
    return Image.blend(img, v, min(1.0, max(0.0, amount)))