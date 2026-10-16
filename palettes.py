from __future__ import annotations

PALETTES: dict[str, list[str]] = {
    "Material": ["#1976D2", "#388E3C", "#FBC02D", "#E64A19", "#7B1FA2"],
    "Tailwind": ["#0EA5E9", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"],
    "Nord": ["#2E3440", "#4C566A", "#88C0D0", "#A3BE8C", "#EBCB8B"],
    "Dracula": ["#282A36", "#BD93F9", "#FF79C6", "#50FA7B", "#F1FA8C"],
    "Solarized": ["#002B36", "#268BD2", "#859900", "#B58900", "#DC322F"],
    "Catppuccin": ["#1E1E2E", "#89B4FA", "#A6E3A1", "#F9E2AF", "#F38BA8"],
    "Mono": ["#0E0E12", "#3A3A42", "#7A7A86", "#BEBEC7", "#F5F5F7"],
    "Sunset": ["#2B1055", "#7597DE", "#F97316", "#FACC15", "#FDE68A"],
}


def names() -> list[str]:
    return list(PALETTES.keys())


def get(name: str) -> list[str]:
    return list(PALETTES.get(name, []))