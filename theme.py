from __future__ import annotations
import customtkinter as ctk


LIGHT = {
    "bg": "#F5F5F7", "panel": "#FFFFFF", "panel_alt": "#FAFAFC",
    "border": "#E5E5EA", "text": "#1C1C1E", "text_muted": "#85858E",
    "accent": "#5C4BA5", "accent_hover": "#6B58C7",
    "accent_soft": "#EAE8FA", "danger": "#C0392B", "success": "#2E8B57",
    "warn": "#B8860B", "canvas": "#FFFFFF",
}
DARK = {
    "bg": "#111114", "panel": "#17171C", "panel_alt": "#1D1D24",
    "border": "#2A2A31", "text": "#E7E7ED", "text_muted": "#8E8E9A",
    "accent": "#8A7BD8", "accent_hover": "#A093E6",
    "accent_soft": "#302C43", "danger": "#E07A6B", "success": "#5CC28E",
    "warn": "#E0B84D", "canvas": "#0E0E12",
}


def colors() -> dict:
    return LIGHT if ctk.get_appearance_mode().lower() == "light" else DARK


def pair(key: str) -> tuple[str, str]:
    """(light, dark) для customtkinter-виджетов."""
    return LIGHT[key], DARK[key]