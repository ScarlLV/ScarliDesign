from __future__ import annotations

# Шаблон = словарь дефолтных настроек редактора.
TEMPLATES: dict[str, dict] = {
    "Минимал-квадрат": {
        "size": (1080, 1080), "bg_mode": "solid", "bg_color": "#0E0E12",
        "title": "quiet\nbrand", "subtitle": "minimal editorial",
        "align": "left", "title_size": 110, "text_color": "#F5F5F7",
        "accent": "bar", "accent_color": "#8A7BD8",
    },
    "Обложка-журнал": {
        "size": (3000, 3000), "bg_mode": "image", "bg_color": "#FFFFFF",
        "title": "Issue #01", "subtitle": "ScarliDesign quarterly",
        "align": "left", "title_size": 260, "text_color": "#111114",
        "accent": "frame", "accent_color": "#E0B84D",
    },
    "Story-gradient": {
        "size": (1080, 1920), "bg_mode": "gradient",
        "bg_color": "#5C4BA5", "bg_color2": "#E07A6B",
        "title": "New\ncollection", "subtitle": "drop 04",
        "align": "center", "title_size": 140, "text_color": "#FFFFFF",
        "accent": "circle", "accent_color": "#FFFFFF",
    },
    "YouTube-thumb": {
        "size": (1280, 720), "bg_mode": "gradient",
        "bg_color": "#111114", "bg_color2": "#302C43",
        "title": "HOW TO\nBUILD", "subtitle": "10 min · 2025",
        "align": "left", "title_size": 130, "text_color": "#FFFFFF",
        "accent": "bar", "accent_color": "#5CC28E",
    },
    "Постер-шрифт": {
        "size": (2480, 3508), "bg_mode": "solid", "bg_color": "#F5F5F7",
        "title": "ТИПО\nГРАФИКА", "subtitle": "poster study",
        "align": "center", "title_size": 320, "text_color": "#111114",
        "accent": "none", "accent_color": "#111114",
    },
    "Banner-широкий": {
        "size": (1920, 600), "bg_mode": "gradient",
        "bg_color": "#0E0E12", "bg_color2": "#5C4BA5",
        "title": "SCARLIDESIGN", "subtitle": "creative workspace",
        "align": "center", "title_size": 130, "text_color": "#FFFFFF",
        "accent": "bar", "accent_color": "#E0B84D",
    },
}


def names() -> list[str]:
    return list(TEMPLATES.keys())


def get(name: str) -> dict:
    return dict(TEMPLATES.get(name, {}))