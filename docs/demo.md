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

# Nesting - Use email if exists, fallback to phone then office. Show 'No contacts if all are None.
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

# Simplified expressions
balance = 500

# Core Python - If-elif bloat
balance = 0
if balance > 0:
    status = "In Credit"
elif balance == 0:
    status = "Zero Balance"
else:
    status = "Overdrawn"

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

# Remove multiple if-elif tests - Clean and easy to read
status_code = None

# Core Python - If-elif bloat
if status_code == "A":
    customer_status = "Active"
elif status_code == "B":
    customer_status = "Blocked"
elif status_code == "C":
    customer_status = "Closed"
elif status_code is None:
    customer_status = "Unknown"
else:
    customer_status = "Other"
    
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
    contact = primary
else:
    contact = backup if backup is not None else primary

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
    message = "Discount applied!"
else:
    message = "No discount available"

# With pynvl
message = nvl2(discount_code, "Discount applied!", "No discount available")  # Discount applied! 
```
---

## 🔹 Pandas Integration

```python
import pandas as pd
from pynvl import pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode

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
```

