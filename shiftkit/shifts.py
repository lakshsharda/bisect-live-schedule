"""Shifts and overtime."""
from .slots import clock, hhmm
from dataclasses import dataclass

WEEKLY_THRESHOLD_MINUTES = 40 * 60
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


@dataclass(frozen=True)
class Shift:
    employee: str
    day: int  # 0 = Monday
    start: int
    end: int


def make_shift(employee: str, day: int, start: str, end: str) -> Shift:
    return Shift(employee, day, hhmm(start), hhmm(end))


def describe(shift: Shift) -> str:
    return f"{DAYS[shift.day]} {clock(shift.start)}-{clock(shift.end)} {shift.employee}"


def shift_minutes(shift: Shift) -> int:
    end = shift.end if shift.end > shift.start else shift.end + 24 * 60  # overnight shifts
    return end - shift.start


def overtime_minutes(worked_minutes: int, threshold_minutes: int) -> int:
    """Minutes worked beyond the threashold."""
    return max(0, worked_minutes - threshold_minutes)
