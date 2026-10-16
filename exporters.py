from __future__ import annotations
import json
from pathlib import Path
from PIL import Image


def save_image(image: Image.Image, path: str | Path, fmt: str = "PNG", dpi: int = 144) -> Path:
    path = Path(path)
    fmt = fmt.upper()
    if fmt == "JPG" and image.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", image.size, (255, 255, 255))
        bg.paste(image, mask=image.split()[-1])
        image = bg
    image.save(path, format=fmt, dpi=(dpi, dpi), quality=95 if fmt == "JPG" else None)
    return path


def palette_to_json(colors: list[str], path: str | Path, name: str = "ScarliDesign Palette") -> Path:
    path = Path(path)
    payload = {"name": name, "colors": colors}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def palette_to_css(colors: list[str], path: str | Path, name: str = "palette") -> Path:
    path = Path(path)
    lines = [":root {"]
    for i, c in enumerate(colors, 1):
        lines.append(f"  --{name}-{i}: {c};")
    lines.append("}")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def palette_to_svg(colors: list[str], path: str | Path) -> Path:
    path = Path(path)
    w, h = 120, 240
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*len(colors)}" height="{h}">']
    for i, c in enumerate(colors):
        parts.append(f'<rect x="{i*w}" y="0" width="{w}" height="{h}" fill="{c}"/>')
        parts.append(f'<text x="{i*w+w/2}" y="{h-20}" font-family="monospace" font-size="14" '
                     f'fill="{"#000" if _is_light(c) else "#fff"}" text-anchor="middle">{c}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def _is_light(hex_color: str) -> bool:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) > 150