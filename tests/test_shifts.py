from shiftkit.shifts import describe, make_shift, overtime_minutes, shift_minutes, weekly_report


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


def full_week(employee, hours_per_day, days=5):
    end = f"{9 + hours_per_day:02d}:00"
    return [make_shift(employee, d, "09:00", end) for d in range(days)]


def test_weekly_report_below_the_threshold_has_no_overtime():
    report = weekly_report(full_week("Ana", 7))  # 35 h
    assert report["Ana"] == {"minutes": 2100, "overtime": 0}


def test_weekly_report_counts_overtime_beyond_forty_hours():
    report = weekly_report(full_week("Ben", 9))  # 45 h
    assert report["Ben"] == {"minutes": 2700, "overtime": 300}


def test_weekly_report_handles_several_employees():
    report = weekly_report(full_week("Ana", 7) + full_week("Ben", 10))  # 35 h and 50 h
    assert list(report) == ["Ana", "Ben"]
    assert report["Ana"]["overtime"] == 0 and report["Ben"]["overtime"] == 600


def test_weekly_report_includes_overnight_shifts():
    shifts = [make_shift("Cy", d, "22:00", "08:00") for d in range(5)]  # 5 x 10 h
    assert weekly_report(shifts)["Cy"] == {"minutes": 3000, "overtime": 600}


def test_weekly_report_of_nothing():
    assert weekly_report([]) == {}
