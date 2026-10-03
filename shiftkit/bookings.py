"""Bookings of resources (rooms, chairs, machines) without double-booking."""
from .slots import Slot, overlaps


class BookingConflict(Exception):
    pass


class BookingBook:
    def __init__(self) -> None:
        self._slots: dict[str, list[Slot]] = {}

    def slots_for(self, resource: str) -> list[Slot]:
        return list(self._slots.get(resource, []))

    def book(self, resource: str, slot: Slot) -> None:
        for existing in self._slots.get(resource, []):
            if overlaps(existing, slot):
                raise BookingConflict(f"{resource}: {slot} overlaps {existing}")
        self._slots.setdefault(resource, []).append(slot)
        self._slots[resource].sort(key=lambda s: s.start)

    def cancel(self, resource: str, slot: Slot) -> None:
        try:
            self._slots.get(resource, []).remove(slot)
        except ValueError:
            raise KeyError(f"{resource}: {slot} is not booked") from None
