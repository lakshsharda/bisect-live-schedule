import pytest

from shiftkit.slots import Slot, clock, free_slots, gap_minutes, hhmm, merge, overlaps


def test_hhmm_parses_times():
    assert hhmm("09:30") == 570
    assert hhmm("00:00") == 0
    assert hhmm("24:00") == 1440


@pytest.mark.parametrize("bad", ["25:00", "09:60"])
def test_hhmm_rejects_bad_times(bad):
    with pytest.raises(ValueError):
        hhmm(bad)


def test_clock_formats_minutes():
    assert clock(570) == "09:30"
    assert clock(5) == "00:05"


def test_slot_duration_and_text():
    slot = Slot(hhmm("09:00"), hhmm("10:30"))
    assert slot.duration == 90 and str(slot) == "09:00-10:30"


def test_slot_must_end_after_it_starts():
    with pytest.raises(ValueError):
        Slot(600, 600)


def test_overlapping_slots():
    assert overlaps(Slot(540, 600), Slot(570, 630))


def test_adjacent_and_separate_slots_do_not_overlap():
    assert not overlaps(Slot(540, 600), Slot(600, 660))
    assert not overlaps(Slot(540, 600), Slot(700, 760))


def test_gap_between_slots():
    assert gap_minutes(Slot(540, 600), Slot(615, 660)) == 15


def test_gap_is_negative_when_slots_overlap():
    assert gap_minutes(Slot(540, 600), Slot(570, 660)) == -30


def test_merge_combines_overlapping_and_touching_slots():
    merged = merge([Slot(600, 660), Slot(540, 610), Slot(660, 700), Slot(800, 820)])
    assert merged == [Slot(540, 700), Slot(800, 820)]


def test_merge_of_nothing():
    assert merge([]) == []


def test_free_slots_around_bookings():
    day = Slot(540, 1020)
    assert free_slots(day, [Slot(600, 660), Slot(720, 780)]) == [Slot(540, 600), Slot(660, 720), Slot(780, 1020)]


def test_free_slots_of_an_empty_day_and_a_full_day():
    day = Slot(540, 1020)
    assert free_slots(day, []) == [day]
    assert free_slots(day, [Slot(500, 1100)]) == []
