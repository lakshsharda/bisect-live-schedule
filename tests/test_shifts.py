from shiftkit.shifts import describe, make_shift, overtime_minutes, shift_minutes


def test_make_shift_parses_times():
    shift = make_shift("Ana", 0, "09:00", "17:00")
    assert (shift.start, shift.end) == (540, 1020)


def test_describe_a_shift():
    assert describe(make_shift("Ana", 2, "09:00", "17:30")) == "Wed 09:00-17:30 Ana"


def test_shift_minutes_for_a_day_shift():
    assert shift_minutes(make_shift("Ana", 0, "09:00", "17:00")) == 480


def test_shift_minutes_for_an_overnight_shift():
    assert shift_minutes(make_shift("Ben", 4, "22:00", "06:00")) == 480


def test_overtime_is_zero_below_the_threshold():
    assert overtime_minutes(2000, 2400) == 0


def test_overtime_counts_minutes_beyond_the_threshold():
    assert overtime_minutes(2700, 2400) == 300
