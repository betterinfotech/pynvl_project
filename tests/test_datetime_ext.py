import datetime as dt
import re
import pytest

import pynvl.datetime_ext as de


D = dt.datetime(2025, 1, 8, 15, 4, 5, 123456)  # Wed, 08-Jan-2025
D_NOON = dt.datetime(2025, 1, 8, 12, 0, 0, 0)
D_MIDNIGHT = dt.datetime(2025, 1, 8, 0, 0, 0, 0)
D_ENDDAY = dt.datetime(2025, 1, 8, 23, 59, 59, 999999)

MONDAY = dt.datetime(2025, 1, 6)  # Monday
SUNDAY = dt.datetime(2025, 1, 5)  # Sunday

# Year boundary / ISO week sanity checks
D_JAN1 = dt.datetime(2025, 1, 1)
D_JAN8 = dt.datetime(2025, 1, 8)
D_DEC31 = dt.datetime(2025, 12, 31)

# Known JDN reference (Gregorian): 2000-01-01 -> 2451545
D_Y2K = dt.datetime(2000, 1, 1)


# ----- basic composition -----
def test_basic_compose():
    assert de.extract(D, "yyyy-mm-dd hh24:mi:ss.ff") == "2025-01-08 15:04:05.123456"
    assert de.extract(D, "dd-mon-rm-yyyy") == "08-jan-I-2025"
    assert de.extract(D, "dd-Mon-rm-YYYY") == "08-Jan-I-2025"
    assert de.extract(D, "DD-MON-RM-YYYY") == "08-JAN-I-2025"


# ----- Case check for (mon/month/day/dy) -----
@pytest.mark.parametrize(
    "fmt,expected",
    [
        ("mon", "jan"),
        ("Mon", "Jan"),
        ("MON", "JAN"),
        ("month", "january"),
        ("Month", "January"),
        ("MONTH", "JANUARY"),
        ("dy", "wed"),
        ("Dy", "Wed"),
        ("DY", "WED"),
        ("day", "wednesday"),
        ("Day", "Wednesday"),
        ("DAY", "WEDNESDAY"),
    ],
)
def test_casing_tokens(fmt, expected):
    # Put the token in a context to ensure only token is replaced
    assert de.extract(D, fmt) == expected


# ----- numeric fields -----
def test_years_slices():
    assert de.extract(D, "yyyy") == "2025"
    assert de.extract(D, "yyy") == "025"
    assert de.extract(D, "yy") == "25"
    assert de.extract(D, "y") == "5"


def test_month_day_numeric():
    assert de.extract(D, "mm") == "01"
    assert de.extract(D, "dd") == "08"
    assert de.extract(D, "ddd") == f"{D.timetuple().tm_yday:03d}"


def test_time_fields_and_fraction():
    assert de.extract(D, "hh24") == "15"
    assert de.extract(D, "hh12") == "03"  # 15 -> 3 PM
    assert de.extract(D_NOON, "hh12") == "12"  # noon -> 12
    assert de.extract(D_MIDNIGHT, "hh12") == "12"  # midnight -> 12
    assert de.extract(D, "mi") == "04"
    assert de.extract(D, "ss") == "05"
    out = de.extract(D, "ff")
    assert re.fullmatch(r"\d{6}", out) and out == f"{D.microsecond:06d}"


def test_seconds_since_midnight():
    assert de.extract(D_MIDNIGHT, "sssss") == "00000"
    assert de.extract(D_ENDDAY, "sssss") == "86399"
    assert de.extract(D, "sssss") == f"{D.hour*3600 + D.minute*60 + D.second:05d}"


# ----- weeks, weekday -----
def test_week_of_year_jan1_style():
    # WW: Jan 1 is week 1, Jan 8 is week 2
    assert de.extract(D_JAN1, "ww") == "01"
    assert de.extract(D_JAN8, "ww") == "02"


def test_week_of_month_w():
    # W: week of month (1..5), counting from day 1
    assert de.extract(dt.datetime(2025, 1, 1), "w") == "1"
    assert de.extract(dt.datetime(2025, 1, 8), "w") == "2"
    assert de.extract(dt.datetime(2025, 1, 31), "w") == "5"


def test_iso_week_iw_matches_python_isocalendar():
    for sample in [
        dt.datetime(2025, 1, 1),
        dt.datetime(2025, 12, 31),
        dt.datetime(2024, 12, 30),  # ISO week overlaps
        dt.datetime(2026, 1, 4),
    ]:
        _, iso_week, _ = sample.isocalendar()
        assert de.extract(sample, "iw") == f"{iso_week:02d}"


def test_weekday_d_mon1_sun7():
    # d: Mon=1..Sun=7
    assert de.extract(MONDAY, "d") == "1"
    assert de.extract(SUNDAY, "d") == "7"


# ----- ISO year family (iyyy/iyy/iy/i) -----
def test_iso_year_family():
    y, w, wd = D.isocalendar()
    assert de.extract(D, "iyyy") == f"{y:04d}"
    assert de.extract(D, "iyy") == f"{y % 1000:03d}"
    assert de.extract(D, "iy") == f"{y % 100:02d}"
    assert de.extract(D, "i") == f"{y % 10}"


# ----- quarter, roman month -----
def test_quarter_and_rm():
    assert de.extract(D, "q") == f"{(D.month - 1) // 3 + 1}"
    assert de.extract(D, "rm") == "I"  # January


# ----- JDN (Julian Day Number) -----
def test_julian_day_number_known_reference():
    # 2000-01-01 -> 2451545
    assert de.extract(D_Y2K, "j") == "2451545"


def test_jdn_increments_by_one_per_day():
    d1 = dt.datetime(2025, 6, 1)
    d2 = dt.datetime(2025, 6, 2)
    j1 = int(de.extract(d1, "j"))
    j2 = int(de.extract(d2, "j"))
    assert j2 - j1 == 1


# ----- literal text and non-tokens stay intact -----
def test_literals_and_non_tokens():
    assert (
        de.extract(D, "Report for dd/mon/yyyy at hh24:mi")
        == "Report for 08/jan/2025 at 15:04"
    )
    # Unknown token 'abc' should pass through unchanged
    assert de.extract(D, "yyyy-abc-dd") == "2025-abc-08"


# ----- case-insensitive token matching, but case applied from pattern -----
@pytest.mark.parametrize(
    "fmt,expected",
    [
        ("dd-mon-yyyy", "08-jan-2025"),
        ("dd-Mon-YYYY", "08-Jan-2025"),
        ("DD-MON-YYYY", "08-JAN-2025"),
        ("dd-month-yyyy", "08-january-2025"),
        ("dd-Month-yyyy", "08-January-2025"),
        ("DD-MONTH-YYYY", "08-JANUARY-2025"),
    ],
)
def test_case_insensitive_match_case_applied(fmt, expected):
    assert de.extract(D, fmt) == expected
