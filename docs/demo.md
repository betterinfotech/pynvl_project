# Demo page

This page gives longer demos of the core `pynvl` functions and their `pd_*` pandas equivalents.
---
## 🔹 NVL
### Substitute a value when a `None` value is encountered.
### `NVL( string1, replace_with)`
```python
from pynvl import nvl

print(nvl(None, 5))      # 5
print(nvl("hello", 99))  # 'hello'

# Nesting - Use email if exists, fallback to phone then office.
email = phone = office = office_extension = None

# Core Python - If-elif bloat
if email is not None:
    primary_contact = email
elif phone is not None:
    primary_contact = phone
elif office_extension is not None:
    primary_contact = office
else:
    primary_contact = "No contacts"

# With pynvl
print(nvl(nvl(nvl(email, phone), office), "No contacts"))
```
---

## 🔹 SIGN
### Returns a value indicating the sign of a number
### `sign(number)`
```python
from pynvl import sign

print(sign(-5))  # -1
print(sign(0))   # 0
print(sign(9))   # 1

balance = 500

# Core Python - If-elif bloat
if balance > 0:
    status_if = "In Credit"
elif balance == 0:
    status_if = "Zero Balance"
else:
    status_if = "Overdrawn"

# With pynvl
status = {1: "In Credit", 0: "Zero Balance", -1: "Overdrawn"}[sign(balance)]
```
---

## 🔹 DECODE
### if-elif-else functionality
### `decode(expression , search , result [, search , result]... [, default] )`
### If no matches are found, the DECODE function will return default.
### If default is omitted, then the DECODE function will return None (if no matches are found).
```python
from pynvl import decode

print(decode("A", "A", "Alpha", "B", "Beta", default="Unknown")) # 'Alpha'
print(decode("Z", "A", "Alpha", "B", "Beta", "Fallback")) # 'Fallback'
print(decode("Z", "A", "Alpha", "B", "Beta")) # None

status_code = None

# Core Python - If-elif bloat
if status_code == "A":
    customer_status_if = "Active"
elif status_code == "B":
    customer_status_if = "Blocked"
elif status_code == "C":
    customer_status_if = "Closed"
elif status_code is None:
    customer_status_if = "Unknown"
else:
    customer_status_if = "Other"
    
# With pynvl
customer_status = decode(
    status_code,
    "A", "Active",
    "B", "Blocked",
    "C", "Closed",
    None, "Unknown",
    default="Other"
)
```
---

## 🔹 NONEIF
### If expr1 and expr2 are equal, the NONEIF function returns NONE. Otherwise, it returns expr1.
### `NONEIF( expr1, expr2 )`
```python
from pynvl import noneif

print(noneif(5, 5))   # None
print(noneif(7, 8))   # 7

primary = "alice@example.com"
backup = "alice@example.com"

# Core Python - If-else bloat
if backup == primary:
    contact_if = primary
else:
    if backup is not None:
        contact_if = backup
    else:
        contact_if = primary

# With pynvl
contact = noneif(backup, primary) or primary # alice@example.com
```
---

## 🔹 NVL2
### Lets you substitutes a value when a null value is encountered as well as when a non-null value is encountered.
### `NVL2( string1, value_if_not_none, value_if_none )`
```python
from pynvl import nvl2

print(nvl2("X", "not-none", "is-none"))  # 'not-none'
print(nvl2(None, "not-none", "is-none")) # 'is-none'

discount_code = "ABC"

# Core Python - If-else bloat
if discount_code is not None:
    message_if = "Discount applied!"
else:
    message_if = "No discount available"

# With pynvl
message = nvl2(discount_code, "Discount applied!", "No discount available")  # Discount applied! 
```
---

## 🔹 COALESCE
## Returns the first non-None expression in the parameter list. If all expressions evaluate to None then coalesce will return None.
### `COALESCE( expr1, expr2, ..., expr_n)`
```python
from pynvl import coalesce

print(coalesce(None, None, 5, 10)) # 5

port_address = None
ip_address = None
mac_address = "A1:B2:C3:D4:E5:F6"

# Core Python - If-elif bloat
if port_address is not None:
    address_if = port_address
elif ip_address is not None:
    address_if = ip_address
elif mac_address is not None:
    address_if = mac_address

# With pynvl
address = coalesce(port_address, ip_address, mac_address) # "A1:B2:C3:D4:E5:F6" 
```
---

## 🔹 EXTRACT
## Returns a formatted string from a datetime object.
## Merges Oracle TO_CHAR() and EXTRACT() to give more intuitive date handling.
### `EXTRACT( expr1, expr2, ..., expr_n)`
```python
from pynvl import extract
from datetime import datetime as dt

today = dt.today()
# Core Python
print(today.strftime("%B").upper())  # e.g. "SEPTEMBER"

# With pynvl
print(extract(today, 'MONTH'))  # e.g. "SEPTEMBER"
"""
| Parameter    | Explanation                                                                 |
|--------------|-----------------------------------------------------------------------------|
| YEAR         | Year, spelled out                                                           |
| YYYY         | 4-digit year                                                                |
| YYY / YY / Y | Last 3, 2, or 1 digit(s) of year                                         |
| IYY / IY / I | Last 3, 2, or 1 digit(s) of ISO year                                     |
| IYYY         | 4-digit year based on the ISO standard                                      |
| Q            | Quarter of year (1, 2, 3, 4; JAN–MAR = 1)                                   |
| MM           | Month (01–12; JAN = 01)                                                     |
| MON          | Abbreviated name of month                                                   |
| MONTH        | Name of month, padded with blanks to length of 9 characters                 |
| RM           | Roman numeral month (I–XII; JAN = I)                                        |
| WW           | Week of year (1–53), where week 1 starts on the first day of the year       |
| W            | Week of month (1–5), where week 1 starts on the first day of the month      |
| IW           | Week of year (1–52 or 1–53) based on the ISO standard                       |
| D            | Day of week (1–7)                                                           |
| DAY          | Name of day                                                                 |
| DD           | Day of month (1–31)                                                         |
| DDD          | Day of year (1–366)                                                         |
| DY           | Abbreviated name of day                                                     |
| J            | Julian day; number of days since January 1, 4712 BC                         |
| HH           | Hour of day (1–12)                                                          |
| HH12         | Hour of day (1–12)                                                          |
| HH24         | Hour of day (0–23)                                                          |
| MI           | Minute (0–59)                                                               |
| SS           | Second (0–59)                                                               |
| SSSSS        | Seconds past midnight (0–86399)                                             |
| FF           | Fractional seconds                                                          |
"""
```

## 🔹 Pandas Integration

```python
import pandas as pd
from pynvl import pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode, pd_coalesce

s = pd.Series([-5, 0, 3, None])

print(pd_sign(s).tolist())
# [-1, 0, 1, None]

print(pd_nvl(s, 99).tolist())
# [-5, 0, 3, 99]

print(pd_nvl2(s, "not-null", "is-null").tolist())
# ['not-null', 'not-null', 'not-null', 'is-null']

print(pd_noneif(s, 0).tolist())
# [-5, None, 3, None]

print(pd_decode(s, -5, "neg", 0, "zero", 3, "pos", default="other").tolist())
# ['neg', 'zero', 'pos', 'other']

a = pd.Series([None, 2, None, 4])
b = pd.Series([1, None, 3, None])
c = pd.Series([9, 9, 9, 9])
out = pd_coalesce(a, b, c)
# [1, 2, 3, 4]
```

