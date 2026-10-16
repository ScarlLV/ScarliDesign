from __future__ import annotations

import json
import sqlite3
from pathlib import Path

APP_DIR = Path.home() / ".scarlidesign"
APP_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = APP_DIR / "scarlidesign.db"
LEGACY_DB_PATH = Path.home() / ".forma_studio" / "forma_studio.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("""CREATE TABLE IF NOT EXISTS palettes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            colors TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
    _import_legacy_palettes()


def _import_legacy_palettes() -> None:
    if not LEGACY_DB_PATH.exists():
        return
    try:
        with get_connection() as target:
            if target.execute("SELECT COUNT(*) FROM palettes").fetchone()[0]:
                return
        with sqlite3.connect(LEGACY_DB_PATH) as source:
            rows = source.execute("SELECT name, colors, created_at FROM palettes ORDER BY id").fetchall()
        cleaned = []
        for name, colors, created_at in rows:
            try:
                parsed = json.loads(colors)
                if isinstance(parsed, list) and parsed:
                    cleaned.append((str(name or "Палитра"), json.dumps(parsed), created_at or "CURRENT_TIMESTAMP"))
            except (TypeError, json.JSONDecodeError):
                continue
        with get_connection() as target:
            target.executemany("INSERT INTO palettes (name, colors, created_at) VALUES (?, ?, ?)", cleaned)
    except (sqlite3.Error, OSError):
        pass


def save_palette(name: str, colors: list[str]) -> int:
    with get_connection() as connection:
        cursor = connection.execute("INSERT INTO palettes (name, colors) VALUES (?, ?)",
                                    (name.strip()[:100] or "Без названия", json.dumps(colors)))
        return int(cursor.lastrowid)


def get_palettes() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT id, name, colors, created_at FROM palettes ORDER BY id DESC").fetchall()
    result = []
    for row in rows:
        try:
            colors = json.loads(row["colors"])
        except json.JSONDecodeError:
            colors = []
        result.append({"id": row["id"], "name": row["name"], "colors": colors, "created_at": row["created_at"]})
    return result


def delete_palette(palette_id: int) -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM palettes WHERE id = ?", (palette_id,))


def get_palette_count() -> int:
    with get_connection() as connection:
        return int(connection.execute("SELECT COUNT(*) FROM palettes").fetchone()[0])

