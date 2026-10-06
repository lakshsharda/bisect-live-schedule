"""Bookings of resources (rooms, chairs, machines) without double-booking."""
from .slots import Slot, gap_minutes, overlaps

DEFAULT_BUFFER_MINUTES = 10


class BookingConflict(Exception):
    pass


class BookingBook:
    def __init__(self, buffer_minutes: int = DEFAULT_BUFFER_MINUTES) -> None:
        self.buffer_minutes = buffer_minutes
        self._slots: dict[str, list[Slot]] = {}

    def slots_for(self, resource: str) -> list[Slot]:
        return list(self._slots.get(resource, []))

    def book(self, resource: str, slot: Slot) -> None:
        for existing in self._slots.get(resource, []):
            if overlaps(existing, slot):
                raise BookingConflict(f"{resource}: {slot} overlaps {existing}")
            earlier, later = (existing, slot) if existing.end <= slot.start else (slot, existing)
            if gap_minutes(earlier, later) < self.buffer_minutes:
                raise BookingConflict(f"{resource}: {slot} is too close to {existing}")
        self._slots.setdefault(resource, []).append(slot)
        self._slots[resource].sort(key=lambda s: s.start)

    def cancel_all_for(self, resource: str) -> int:
        """Remove every booking of a resource; returns how many were removed."""
        return len(self._slots.pop(resource, []))

    def cancel(self, resource: str, slot: Slot) -> None:
        try:
            self._slots.get(resource, []).remove(slot)
        except ValueError:
            raise KeyError(f"{resource}: {slot} is not booked") from None
