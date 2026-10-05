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

    @property
    def minutes(self) -> int:
        end = self.end if self.end > self.start else self.end + 24 * 60  # overnight shifts
        return end - self.start


def make_shift(employee: str, day: int, start: str, end: str) -> Shift:
    return Shift(employee, day, hhmm(start), hhmm(end))


def describe(shift: Shift) -> str:
    return f"{DAYS[shift.day]} {clock(shift.start)}-{clock(shift.end)} {shift.employee}"


def is_night_shift(shift: Shift) -> bool:
    """A shift that starts at 22:00 or later, ends by 06:00, or runs past midnight."""
    return shift.start >= hhmm("22:00") or shift.end <= hhmm("06:00") or shift.end <= shift.start


def shift_minutes(shift: Shift) -> int:
    return shift.minutes


def overtime_minutes(worked_minutes: int, threshold_minutes: int) -> int:
    """Minutes worked beyond the threashold."""
    return max(0, worked_minutes - threshold_minutes)


def weekly_report(shifts: list[Shift]) -> dict[str, dict[str, int]]:
    """Total and overtime minutes per employee for one week."""
    totals: dict[str, int] = {}
    for shift in shifts:
        totals[shift.employee] = totals.get(shift.employee, 0) + shift.minutes
    return {
        employee: {"minutes": minutes, "overtime": overtime_minutes(minutes, WEEKLY_THRESHOLD_MINUTES)}
        for employee, minutes in sorted(totals.items())
    }
