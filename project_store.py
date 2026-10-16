from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

APP_DIR = Path.home() / ".scarlidesign"
PROJECTS_DIR = APP_DIR / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def _slug(value: str) -> str:
    value = re.sub(r"[^\w\- ]+", "", value, flags=re.UNICODE).strip().lower()
    value = re.sub(r"[\s\-]+", "_", value)
    return value[:60] or "design"


def save_project(data: dict, path: str | Path | None = None) -> Path:
    payload = dict(data)
    payload["schema_version"] = 1
    payload["updated_at"] = datetime.now().isoformat(timespec="seconds")
    if path:
        target = Path(path)
        if target.suffix.lower() != ".scarli":
            target = target.with_suffix(".scarli")
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = PROJECTS_DIR / f"{_slug(payload.get('name', 'design'))}_{stamp}.scarli"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def load_project(path: str | Path) -> dict:
    source = Path(path)
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") not in (None, 1):
        raise ValueError("Файл проекта имеет неподдерживаемый формат.")
    data["_file_path"] = str(source)
    return data


def list_projects() -> list[dict]:
    results = []
    for path in PROJECTS_DIR.glob("*.scarli"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            stat = path.stat()
            results.append({"path": path, "name": data.get("name") or path.stem,
                            "size": stat.st_size, "updated_at": data.get("updated_at") or datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="minutes"),
                            "width": data.get("width", 1080), "height": data.get("height", 1080)})
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(results, key=lambda item: item["updated_at"], reverse=True)


def delete_project(path: str | Path) -> None:
    target = Path(path).resolve()
    if target.parent.resolve() != PROJECTS_DIR.resolve():
        raise ValueError("Можно удалять только проекты из библиотеки ScarliDesign.")
    target.unlink(missing_ok=True)
