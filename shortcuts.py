from __future__ import annotations
from typing import Callable


def bind(app, sequence: str, callback: Callable) -> str:
    """Глобальный hotkey на окно."""
    return app.bind_all(sequence, lambda e: callback(), add="+")