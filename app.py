from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

from core import i18n
from core.database import initialize_database
from views.dashboard import DashboardView
from views.color_lab import ColorLabView
from views.editor import EditorView
from views.image_lab import ImageLabView
from views.projects import ProjectsView

APP_NAME = "ScarliDesign"
VERSION = "0.1"


class ScarliDesignApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title(f"{APP_NAME} · {VERSION}")
        self.geometry("1300x820")
        self.minsize(1000, 680)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        self.current_view = None
        self.current_name = "home"

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.show_view("home")

    def _build_sidebar(self):
        sb = self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0,
                                          fg_color=("#FFFFFF", "#17171C"))
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        self.brand = ctk.CTkLabel(sb, text=APP_NAME,
                                   font=ctk.CTkFont(size=22, weight="bold"))
        self.brand.pack(anchor="w", padx=20, pady=(24, 2))
        self.sub = ctk.CTkLabel(sb, text=f"v{VERSION}  ·  {i18n.t('app.tagline')}",
                                 font=ctk.CTkFont(size=10, weight="bold"),
                                 text_color=("#85858E", "#8E8E9A"))
        self.sub.pack(anchor="w", padx=21, pady=(0, 22))

        self.nav_buttons = {}
        self._nav_order = ["home", "color_lab", "editor", "image_lab", "library"]
        for key in self._nav_order:
            b = ctk.CTkButton(sb, text="", anchor="w", height=42, corner_radius=9,
                              font=ctk.CTkFont(size=13),
                              fg_color="transparent",
                              hover_color=("#F0EFF8", "#292833"),
                              text_color=("#33333B", "#E7E7ED"),
                              command=lambda k=key: self.show_view(k))
            b.pack(fill="x", padx=11, pady=3)
            self.nav_buttons[key] = b

        bottom = ctk.CTkFrame(sb, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=12, pady=(0, 12))

        self.lang_button = ctk.CTkButton(bottom, text="", height=32,
                                          fg_color="transparent", border_width=1,
                                          command=self.toggle_language)
        self.lang_button.pack(fill="x", pady=(0, 6))

        self.theme_button = ctk.CTkButton(bottom, text="", height=32,
                                           fg_color="transparent", border_width=1,
                                           command=self.toggle_theme)
        self.theme_button.pack(fill="x")

        self._apply_language()

    def _apply_language(self):
        icons = {"home": "⌂", "color_lab": "◉", "editor": "▧",
                 "image_lab": "▤", "library": "▦"}
        keys = {"home": "nav.home", "color_lab": "nav.color_lab",
                "editor": "nav.editor", "image_lab": "nav.image_lab",
                "library": "nav.library"}
        for k, b in self.nav_buttons.items():
            b.configure(text=f"{icons[k]}   {i18n.t(keys[k])}")

        mode = ctk.get_appearance_mode().lower()
        self.theme_button.configure(
            text=i18n.t("theme.to_dark") if mode == "light"
            else i18n.t("theme.to_light")
        )
        self.lang_button.configure(text=i18n.t("lang.button"))
        self.sub.configure(text=f"v{VERSION}  ·  {i18n.t('app.tagline')}")

    def toggle_theme(self):
        mode = "light" if ctk.get_appearance_mode().lower() == "dark" else "dark"
        ctk.set_appearance_mode(mode)
        self._apply_language()

    def toggle_language(self):
        i18n.toggle_language()
        self._apply_language()
        self.show_view(self.current_name)

    def show_view(self, name, project_path=None):
        self.current_name = name
        for child in self.content.winfo_children():
            child.destroy()

        for key, button in self.nav_buttons.items():
            active = key == name
            button.configure(
                fg_color=("#EAE8FA", "#302C43") if active else "transparent",
                text_color=("#5C4BA5", "#D2C9FF") if active
                else ("#33333B", "#E7E7ED"),
            )

        if name == "home":
            view = DashboardView(self.content, self.show_view)
        elif name == "color_lab":
            view = ColorLabView(self.content)
        elif name == "editor":
            view = EditorView(self.content)
            if project_path:
                view.load_project_file(project_path)
        elif name == "image_lab":
            view = ImageLabView(self.content)
        else:
            view = ProjectsView(self.content, self.show_view)

        view.grid(row=0, column=0, sticky="nsew")
        self.current_view = view

    def _on_close(self):
        try:
            v = self.current_view
            job = getattr(v, "_render_job", None) if v else None
            if job:
                self.after_cancel(job)
        except Exception:
            pass
        self.destroy()


def main():
    try:
        initialize_database()
    except Exception as exc:
        print("DB init failed:", exc)
    try:
        app = ScarliDesignApp()
        app.mainloop()
    except Exception as exc:
        try:
            messagebox.showerror(f"{APP_NAME} — error",
                                 i18n.t("dlg.error", error=exc))
        except Exception:
            raise


if __name__ == "__main__":
    main()