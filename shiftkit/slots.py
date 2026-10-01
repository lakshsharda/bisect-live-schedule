"""Time slots measured in minutes since midnight."""
from dataclasses import dataclass


def hhmm(text: str) -> int:
    """'09:30' -> 570."""
    hours, _, minutes = text.partition(":")
    h, m = int(hours), int(minutes)
    if not (0 <= h <= 24 and 0 <= m < 60) or (h == 24 and m):
        raise ValueError(f"not a time of day: {text!r}")
    return h * 60 + m


def clock(minutes: int) -> str:
    """570 -> '09:30'."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


@dataclass(frozen=True)
class Slot:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError("a slot must end after it starts")

    @property
    def duration(self) -> int:
        return self.end - self.start

    def __str__(self) -> str:
        return f"{clock(self.start)}-{clock(self.end)}"


def overlaps(a: Slot, b: Slot) -> bool:
    return a.start < b.end and b.start < a.end


def gap_minutes(earlier: Slot, later: Slot) -> int:
    """Minutes between the end of `earlier` and the start of `later` (negative if they overlap)."""
    return later.start - earlier.end


def merge(slots: list[Slot]) -> list[Slot]:
    """Combine overlapping or touching slots into the smallest sorted list."""
    merged: list[Slot] = []
    for slot in sorted(slots, key=lambda s: s.start):
        if merged and slot.start <= merged[-1].end:
            merged[-1] = Slot(merged[-1].start, max(merged[-1].end, slot.end))
        else:
            merged.append(slot)
    return merged
