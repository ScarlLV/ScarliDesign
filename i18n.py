from __future__ import annotations

import locale as _locale

_STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "app.tagline": "local mode",
        "nav.home": "Home",
        "nav.color_lab": "Color Lab",
        "nav.editor": "Editor",
        "nav.image_lab": "Image Lab",
        "nav.library": "Library",
        "theme.to_light": "☼  Light theme",
        "theme.to_dark": "☾  Dark theme",
        "lang.button": "🌐  УКР",

        "editor.header": "EDITOR",
        "editor.canvas": "Canvas",
        "editor.palettes": "Palettes",
        "editor.recent": "Recent",
        "editor.background": "Background",
        "editor.color1": "Color 1",
        "editor.color2": "Color 2",
        "editor.load_image": "Load image…",
        "editor.dim": "Dim",
        "editor.vignette": "Vignette",
        "editor.title": "Title",
        "editor.subtitle": "Subtitle",
        "editor.caption": "Caption",
        "editor.align": "Align",
        "editor.title_size": "Title size",
        "editor.subtitle_size": "Subtitle size",
        "editor.caption_size": "Caption size",
        "editor.title_y": "Title Y",
        "editor.line_height": "Line height",
        "editor.tracking": "Tracking",
        "editor.uppercase": "UPPERCASE",
        "editor.text_color": "Text color",
        "editor.accent_color": "Accent color",
        "editor.eyedropper": "🎨 Eyedropper",
        "editor.accent": "Accent",
        "editor.shadow": "Shadow",
        "editor.outline": "Outline",
        "editor.safe_area": "Safe area",
        "editor.random": "🎲 Random style",
        "editor.export_png": "💾 Export PNG",
        "editor.export_jpg": "💾 Export JPG",
        "editor.save_project": "📦 Save .scarli",
        "editor.open_project": "📂 Open .scarli",
        "editor.status.ready": "Ready",

        "dlg.export": "Export",
        "dlg.export_saved": "Saved:\n{path}",
        "dlg.project": "Project",
        "dlg.project_saved": "Project saved.",
        "dlg.image": "Image",
        "dlg.error": "Application failed to start.\n\n{error}",

        "home.title": "Dashboard",
        "home.subtitle": "Quick overview of your local workspace.",
        "home.projects": "Projects",
        "home.palettes": "Palettes",
        "home.open_editor": "Open Editor",
        "home.open_color": "Open Color Lab",
        "home.open_library": "Open Library",

        "cl.title": "Color Lab",
        "cl.subtitle": "Generate harmonies, save locally, export to CSS / JSON.",
        "cl.base": "Base color",
        "cl.scheme": "Scheme",
        "cl.generate": "Generate",
        "cl.copy_all": "Copy all",
        "cl.copy_hex": "Copy HEX",
        "cl.save": "Save palette",
        "cl.export_json": "Export JSON",
        "cl.export_css": "Export CSS",
        "cl.scheme.analogous": "Analogous",
        "cl.scheme.complementary": "Complementary",
        "cl.scheme.triadic": "Triadic",
        "cl.scheme.split": "Split-complementary",
        "cl.scheme.tetradic": "Tetradic",
        "cl.scheme.mono": "Monochrome",
        "cl.scheme.random": "Random",
        "cl.saved": "Palette saved.",
        "cl.copied": "Copied: {value}",

        "il.title": "Image Lab",
        "il.subtitle": "Load a reference, tweak it, export a copy.",
        "il.open": "Open image…",
        "il.brightness": "Brightness",
        "il.contrast": "Contrast",
        "il.saturation": "Saturation",
        "il.filter": "Filter",
        "il.filter.none": "None",
        "il.filter.gray": "Grayscale",
        "il.filter.sepia": "Sepia",
        "il.filter.soft": "Soft",
        "il.filter.sharpen": "Sharpen",
        "il.rotate": "Rotate 90°",
        "il.flip": "Flip H",
        "il.export": "Export copy",
        "il.info": "Size: {w} × {h}",
        "il.no_image": "No image loaded.",
        "il.exported": "Saved:\n{path}",

        "lib.title": "Library",
        "lib.subtitle": "Saved projects and palettes.",
        "lib.projects": "Projects",
        "lib.palettes": "Palettes",
        "lib.open": "Open",
        "lib.delete": "Delete",
        "lib.copy": "Copy HEX",
        "lib.empty": "Nothing here yet.",
        "lib.confirm_delete": "Delete this item?",
    },
    "uk": {
        "app.tagline": "локальний режим",
        "nav.home": "Головна",
        "nav.color_lab": "Color Lab",
        "nav.editor": "Редактор",
        "nav.image_lab": "Image Lab",
        "nav.library": "Бібліотека",
        "theme.to_light": "☼  Світла тема",
        "theme.to_dark": "☾  Темна тема",
        "lang.button": "🌐  ENG",

        "editor.header": "РЕДАКТОР",
        "editor.canvas": "Полотно",
        "editor.palettes": "Палітри",
        "editor.recent": "Нещодавні",
        "editor.background": "Фон",
        "editor.color1": "Колір 1",
        "editor.color2": "Колір 2",
        "editor.load_image": "Завантажити зображення…",
        "editor.dim": "Затемнення",
        "editor.vignette": "Віньєтка",
        "editor.title": "Заголовок",
        "editor.subtitle": "Підзаголовок",
        "editor.caption": "Підпис",
        "editor.align": "Вирівнювання",
        "editor.title_size": "Розмір заголовка",
        "editor.subtitle_size": "Розмір підзаголовка",
        "editor.caption_size": "Розмір підпису",
        "editor.title_y": "Y заголовка",
        "editor.line_height": "Міжрядковий",
        "editor.tracking": "Трекінг",
        "editor.uppercase": "ВЕЛИКІ ЛІТЕРИ",
        "editor.text_color": "Колір тексту",
        "editor.accent_color": "Колір акценту",
        "editor.eyedropper": "🎨 Піпетка",
        "editor.accent": "Акцент",
        "editor.shadow": "Тінь",
        "editor.outline": "Обведення",
        "editor.safe_area": "Безпечна зона",
        "editor.random": "🎲 Випадковий стиль",
        "editor.export_png": "💾 Експорт PNG",
        "editor.export_jpg": "💾 Експорт JPG",
        "editor.save_project": "📦 Зберегти .scarli",
        "editor.open_project": "📂 Відкрити .scarli",
        "editor.status.ready": "Готово",

        "dlg.export": "Експорт",
        "dlg.export_saved": "Збережено:\n{path}",
        "dlg.project": "Проєкт",
        "dlg.project_saved": "Проєкт збережено.",
        "dlg.image": "Зображення",
        "dlg.error": "Не вдалося запустити застосунок.\n\n{error}",

        "home.title": "Панель",
        "home.subtitle": "Короткий огляд локального простору.",
        "home.projects": "Проєкти",
        "home.palettes": "Палітри",
        "home.open_editor": "Відкрити редактор",
        "home.open_color": "Відкрити Color Lab",
        "home.open_library": "Відкрити бібліотеку",

        "cl.title": "Color Lab",
        "cl.subtitle": "Генеруй гармонії, зберігай локально, експортуй у CSS / JSON.",
        "cl.base": "Базовий колір",
        "cl.scheme": "Схема",
        "cl.generate": "Згенерувати",
        "cl.copy_all": "Копіювати все",
        "cl.copy_hex": "Копіювати HEX",
        "cl.save": "Зберегти палітру",
        "cl.export_json": "Експорт JSON",
        "cl.export_css": "Експорт CSS",
        "cl.scheme.analogous": "Аналогова",
        "cl.scheme.complementary": "Комплементарна",
        "cl.scheme.triadic": "Тріада",
        "cl.scheme.split": "Розщеплено-комплементарна",
        "cl.scheme.tetradic": "Тетрада",
        "cl.scheme.mono": "Монохромна",
        "cl.scheme.random": "Випадкова",
        "cl.saved": "Палітру збережено.",
        "cl.copied": "Скопійовано: {value}",

        "il.title": "Image Lab",
        "il.subtitle": "Завантаж референс, налаштуй, експортуй копію.",
        "il.open": "Відкрити зображення…",
        "il.brightness": "Яскравість",
        "il.contrast": "Контраст",
        "il.saturation": "Насиченість",
        "il.filter": "Фільтр",
        "il.filter.none": "Немає",
        "il.filter.gray": "Ч/Б",
        "il.filter.sepia": "Сепія",
        "il.filter.soft": "М'якість",
        "il.filter.sharpen": "Різкість",
        "il.rotate": "Повернути 90°",
        "il.flip": "Відзеркалити",
        "il.export": "Експорт копії",
        "il.info": "Розмір: {w} × {h}",
        "il.no_image": "Зображення не завантажено.",
        "il.exported": "Збережено:\n{path}",

        "lib.title": "Бібліотека",
        "lib.subtitle": "Збережені проєкти та палітри.",
        "lib.projects": "Проєкти",
        "lib.palettes": "Палітри",
        "lib.open": "Відкрити",
        "lib.delete": "Видалити",
        "lib.copy": "Копіювати HEX",
        "lib.empty": "Тут поки нічого немає.",
        "lib.confirm_delete": "Видалити цей елемент?",
    },
}

_LANG = "en"


def _detect() -> str:
    try:
        loc = (_locale.getdefaultlocale()[0] or "").lower()
    except Exception:
        loc = ""
    return "uk" if loc.startswith("uk") else "en"


_LANG = _detect()


def get_language() -> str:
    return _LANG


def set_language(code: str) -> None:
    global _LANG
    if code in _STRINGS:
        _LANG = code


def toggle_language() -> str:
    global _LANG
    _LANG = "uk" if _LANG == "en" else "en"
    return _LANG


def t(key: str, **fmt) -> str:
    table = _STRINGS.get(_LANG, _STRINGS["en"])
    value = table.get(key) or _STRINGS["en"].get(key, key)
    if fmt:
        try:
            return value.format(**fmt)
        except Exception:
            return value
    return value