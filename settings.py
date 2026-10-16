from __future__ import annotations
import json
from pathlib import Path

SETTINGS_PATH = Path.home() / ".scarlidesign" / "settings.json"
DEFAULTS = {
    "appearance": "dark",
    "accent": "blue",
    "autosave_sec": 60,
    "grid": False,
    "rulers": True,
    "show_welcome": True,
    "export_png_dpi": 144,
}


def load_settings() -> dict:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULTS)
        return dict(DEFAULTS)
    try:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        merged = {**DEFAULTS, **data}
        return merged
    except Exception:
        return dict(DEFAULTS)


def save_settings(values: dict) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(values, indent=2, ensure_ascii=False), encoding="utf-8")


def set_setting(key: str, value) -> dict:
    data = load_settings()
    data[key] = value
    save_settings(data)
    return data