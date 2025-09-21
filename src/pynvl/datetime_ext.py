from __future__ import annotations

import re
import datetime as _dt
from typing import Callable, Dict

__all__ = ["extract"]

def _iso_parts(d: _dt.datetime) -> tuple[int, int, int]:
    iso = d.isocalendar()
    try:
        return int(iso.year), int(iso.week), int(iso.weekday)
    except AttributeError:
        y, w, wd = iso
        return int(y), int(w), int(wd)

def _week_of_year_jan1(d: _dt.datetime) -> int:
    doy = d.timetuple().tm_yday  # 1..366
    return ((doy - 1) // 7) + 1

def _week_of_month(d: _dt.datetime) -> int:
    return ((d.day - 1) // 7) + 1

def _seconds_since_midnight(d: _dt.datetime) -> int:
    return d.hour * 3600 + d.minute * 60 + d.second

_ROMANS = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]

def _julian_day_number(d: _dt.datetime) -> int:
    # Fliegel–Van Flandern (Gregorian date -> JDN)
    y, m, dd = d.year, d.month, d.day
    a  = (14 - m) // 12
    y_ = y + 4800 - a
    m_ = m + 12*a - 3
    return dd + ((153*m_ + 2)//5) + 365*y_ + (y_//4) - (y_//100) + (y_//400) - 32045

# Longest tokens first to avoid partial matches (e.g. sssss before ss, ww before w)
_TOKEN_RE = re.compile(
    r"(?:" 
    r"iyyy|yyyy|month|hh24|hh12|sssss|"
    r"iyy|yyy|ddd|mon|day|hh|mi|ff|iw|ww|"
    r"iy|yy|rm|mm|dd|dy|w|d|q|j|ss|y|i"
    r")",
    flags=re.IGNORECASE
)

def _apply_case(pattern_token: str, text: str) -> str:
    """Match the case style of the token: lower / UPPER / Title."""
    if pattern_token.isupper():
        return text.upper()
    if pattern_token.islower():
        return text.lower()
    if pattern_token[:1].isupper() and pattern_token[1:].islower():
        return text[:1].upper() + text[1:].lower()
    return text

def extract(d: _dt.datetime, fmt: str) -> str:
    """
    Oracle-like date formatting with case-sensitive tokens:
      mon -> jan, Mon -> Jan, MON -> JAN
      month/day/dy behave similarly. 'rm' is Roman month I..XII (always uppercase).
    """
    if not isinstance(d, _dt.datetime):
        raise TypeError("dt must be a datetime.datetime")

    iso_year, iso_week, iso_wday = _iso_parts(d)
    year4 = f"{d.year:04d}"

    handlers: Dict[str, Callable[[], str]] = {
        # ISO year
        "iyyy": lambda: f"{iso_year:04d}",
        "iyy":  lambda: f"{iso_year % 1000:03d}",
        "iy":   lambda: f"{iso_year % 100:02d}",
        "i":    lambda: f"{iso_year % 10}",
        # Gregorian years
        "yyyy": lambda: year4,
        "yyy":  lambda: year4[-3:],
        "yy":   lambda: year4[-2:],
        "y":    lambda: year4[-1:],
        # Month
        "mm":    lambda: f"{d.month:02d}",
        "mon":   lambda: d.strftime("%b").lower(),   # jan
        "month": lambda: d.strftime("%B").lower(),   # january
        "rm":    lambda: _ROMANS[d.month - 1],       # I..XII
        # Day & DOY
        "dd":    lambda: f"{d.day:02d}",
        "ddd":   lambda: f"{d.timetuple().tm_yday:03d}",
        "dy":    lambda: d.strftime("%a").lower(),   # wed
        "day":   lambda: d.strftime("%A").lower(),   # wednesday
        # Hours
        "hh24":  lambda: f"{d.hour:02d}",
        "hh12":  lambda: f"{(d.hour % 12) or 12:02d}",
        "hh":    lambda: f"{(d.hour % 12) or 12:02d}",
        # Minutes/Seconds/Fraction
        "mi":    lambda: f"{d.minute:02d}",
        "ss":    lambda: f"{d.second:02d}",
        "ff":    lambda: f"{d.microsecond:06d}",
        # Weeks / weekday
        "iw":    lambda: f"{iso_week:02d}",
        "ww":    lambda: f"{_week_of_year_jan1(d):02d}",
        "w":     lambda: f"{_week_of_month(d)}",
        "d":     lambda: f"{iso_wday}",               # Mon=1..Sun=7
        # Quarter
        "q":     lambda: f"{(d.month - 1) // 3 + 1}",
        # Julian day number
        "j":     lambda: f"{_julian_day_number(d)}",
        # Seconds since midnight
        "sssss": lambda: f"{_seconds_since_midnight(d):05d}",
    }

    def _sub(m: re.Match) -> str:
        tok_raw = m.group(0)
        key = tok_raw.lower()
        out = handlers[key]()
        if key == "rm":
            return out  # always uppercase
        return _apply_case(tok_raw, out)

    return _TOKEN_RE.sub(_sub, fmt)

if __name__ == "__main__":
    d = _dt.datetime(2025, 1, 8, 15, 4, 5, 123456)
    print(extract(d, "yyyy-mm-dd hh24:mi:ss.ff"))   # 2025-01-08 15:04:05.123456
    print(extract(d, "dd-mon-rm-yyyy"))             # 08-jan-I-2025
    print(extract(d, "dd-Mon-rm-YYYY"))             # 08-Jan-I-2025
    print(extract(d, "dd-month-yyyy"))              # 08-january-2025
    print(extract(d, "dd-Month-yyyy"))              # 08-January-2025
    print(extract(d, "DD-MONTH-YYYY"))              # 08-JANUARY-2025
    print(extract(d, "Day"))                        # Wednesday
