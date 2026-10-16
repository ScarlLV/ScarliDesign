from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class HistoryEntry:
    label: str
    state: dict


@dataclass
class History:
    limit: int = 50
    _undo: list[HistoryEntry] = field(default_factory=list)
    _redo: list[HistoryEntry] = field(default_factory=list)
    on_change: Callable[[], None] | None = None

    def push(self, label: str, state: dict) -> None:
        if self._undo and self._undo[-1].state == state:
            return
        self._undo.append(HistoryEntry(label, dict(state)))
        if len(self._undo) > self.limit:
            self._undo.pop(0)
        self._redo.clear()
        if self.on_change:
            self.on_change()

    def undo(self, current: dict) -> dict | None:
        if not self._undo:
            return None
        entry = self._undo.pop()
        self._redo.append(HistoryEntry(entry.label, dict(current)))
        if self.on_change:
            self.on_change()
        return entry.state

    def redo(self, current: dict) -> dict | None:
        if not self._redo:
            return None
        entry = self._redo.pop()
        self._undo.append(HistoryEntry(entry.label, dict(current)))
        if self.on_change:
            self.on_change()
        return entry.state

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    def labels(self) -> tuple[str | None, str | None]:
        u = self._undo[-1].label if self._undo else None
        r = self._redo[-1].label if self._redo else None
        return u, r