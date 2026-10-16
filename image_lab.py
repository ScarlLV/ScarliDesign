from __future__ import annotations

from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageFilter, ImageTk

from core import i18n


FILTERS = {
    "il.filter.none": None,
    "il.filter.gray": "gray",
    "il.filter.sepia": "sepia",
    "il.filter.soft": "soft",
    "il.filter.sharpen": "sharpen",
}


class ImageLabView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.original: Image.Image | None = None
        self.rotated = 0
        self.flipped = False
        self._photo = None

        self._build_sidebar()
        self._build_canvas()

    def _build_sidebar(self):
        side = ctk.CTkScrollableFrame(self, width=280, fg_color=("#FFFFFF", "#17171C"))
        side.grid(row=0, column=0, sticky="nsw", padx=(0, 1))

        ctk.CTkLabel(side, text=i18n.t("il.title"),
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=("#85858E", "#8E8E9A")
                     ).pack(anchor="w", padx=14, pady=(14, 8))

        ctk.CTkButton(side, text=i18n.t("il.open"),
                      command=self.open_image).pack(fill="x", padx=14)

        self.brightness = self._slider(side, "il.brightness", 0.2, 2.0, 1.0)
        self.contrast = self._slider(side, "il.contrast", 0.2, 2.0, 1.0)
        self.saturation = self._slider(side, "il.saturation", 0.0, 2.0, 1.0)

        ctk.CTkLabel(side, text=i18n.t("il.filter")).pack(anchor="w", padx=14, pady=(10, 2))
        self.filter_var = ctk.StringVar(value=i18n.t("il.filter.none"))
        ctk.CTkOptionMenu(side, values=[i18n.t(k) for k in FILTERS],
                          variable=self.filter_var,
                          command=lambda _v: self.update_preview()
                          ).pack(fill="x", padx=14)

        row = ctk.CTkFrame(side, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=10)
        ctk.CTkButton(row, text=i18n.t("il.rotate"), command=self.rotate
                      ).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ctk.CTkButton(row, text=i18n.t("il.flip"), command=self.flip
                      ).pack(side="left", expand=True, fill="x", padx=(3, 0))

        ctk.CTkButton(side, text=i18n.t("il.export"), command=self.export
                      ).pack(fill="x", padx=14, pady=10)

        self.info = ctk.CTkLabel(side, text=i18n.t("il.no_image"),
                                  text_color=("#85858E", "#8E8E9A"))
        self.info.pack(anchor="w", padx=14, pady=(0, 14))

    def _slider(self, parent, key, frm, to, init):
        ctk.CTkLabel(parent, text=i18n.t(key)).pack(anchor="w", padx=14, pady=(8, 0))
        s = ctk.CTkSlider(parent, from_=frm, to=to, command=lambda _v: self.update_preview())
        s.set(init)
        s.pack(fill="x", padx=14)
        return s

    def _build_canvas(self):
        wrap = ctk.CTkFrame(self, fg_color=("#EAEAEE", "#0B0B0E"))
        wrap.grid(row=0, column=1, sticky="nsew")
        wrap.grid_rowconfigure(0, weight=1)
        wrap.grid_columnconfigure(0, weight=1)
        from tkinter import Canvas
        self.canvas = Canvas(wrap, background="#0B0B0E", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _e: self.update_preview())

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if not path:
            return
        try:
            self.original = Image.open(path).convert("RGB")
            self.rotated = 0
            self.flipped = False
            self.info.configure(text=i18n.t("il.info", w=self.original.width,
                                             h=self.original.height))
            self.update_preview()
        except Exception as exc:
            messagebox.showerror(i18n.t("il.title"), str(exc))

    def rotate(self):
        if not self.original:
            return
        self.rotated = (self.rotated + 90) % 360
        self.update_preview()

    def flip(self):
        if not self.original:
            return
        self.flipped = not self.flipped
        self.update_preview()

    def _processed(self) -> Image.Image | None:
        if not self.original:
            return None
        img = self.original.copy()
        if self.rotated:
            img = img.rotate(-self.rotated, expand=True)
        if self.flipped:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img = ImageEnhance.Brightness(img).enhance(float(self.brightness.get()))
        img = ImageEnhance.Contrast(img).enhance(float(self.contrast.get()))
        img = ImageEnhance.Color(img).enhance(float(self.saturation.get()))

        f_key = None
        for k, v in FILTERS.items():
            if i18n.t(k) == self.filter_var.get():
                f_key = v
                break
        if f_key == "gray":
            img = img.convert("L").convert("RGB")
        elif f_key == "sepia":
            img = img.convert("L").convert("RGB")
            sepia = Image.new("RGB", img.size)
            px = img.load()
            sp = sepia.load()
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b = px[x, y]
                    sp[x, y] = (min(255, int(r * 1.07 + 30)),
                                min(255, int(g * 0.95 + 10)),
                                min(255, int(b * 0.75)))
            img = sepia
        elif f_key == "soft":
            img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
        elif f_key == "sharpen":
            img = img.filter(ImageFilter.SHARPEN)
        return img

    def update_preview(self):
        img = self._processed()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        self.canvas.delete("all")
        if img is None or cw < 20 or ch < 20:
            return
        scale = min((cw - 40) / img.width, (ch - 40) / img.height, 1.0)
        pw, ph = max(1, int(img.width * scale)), max(1, int(img.height * scale))
        prev = img.resize((pw, ph), Image.LANCZOS)
        self._photo = ImageTk.PhotoImage(prev)
        ox, oy = (cw - pw) // 2, (ch - ph) // 2
        self.canvas.create_image(ox, oy, anchor="nw", image=self._photo)

    def export(self):
        img = self._processed()
        if img is None:
            messagebox.showwarning(i18n.t("il.title"), i18n.t("il.no_image"))
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")]
        )
        if not path:
            return
        try:
            if path.lower().endswith(".jpg"):
                img.save(path, quality=95)
            else:
                img.save(path)
            messagebox.showinfo(i18n.t("il.title"),
                                i18n.t("il.exported", path=path))
        except Exception as exc:
            messagebox.showerror(i18n.t("il.title"), str(exc))