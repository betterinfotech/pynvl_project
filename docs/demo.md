# 🧪 Demo page

This page gives longer demos of the core `pynvl` functions and their `pd_*` pandas equivalents.
---
## 🔹 NVL
```python
from pynvl import nvl

print(nvl(None, 5))      # 5
print(nvl("hello", 99))  # 'hello'

# Nesting - Use email if exists, fallback to phone then office. Show 'No contacts if all are None.
print(nvl(nvl(nvl(email, phone), office), "No contacts"))

# Python core
if email is not None:
    primary_contact = email
elif phone is not None:
    primary_contact = phone
elif office_extension is not None:
    primary_contact = office
else:
    primary_contact = "No contacts"
```
---

## 🔹 SIGN
```python
from pynvl import sign

print(sign(-5))  # -1
print(sign(0))   # 0
print(sign(9))   # 1

# Simplified expressions
status = {1: "In Credit", 0: "Zero Balance", -1: "Overdrawn"}[sign(balance)]

# If-elif code bloat
if balance > 0:
    status = "In Credit"
elif balance == 0:
    status = "Zero Balance"
else:
    status = "Overdrawn"
```
---

## 🔹 DECODE
```python
from pynvl import decode

print(decode("A", "A", "Alpha", "B", "Beta", default="Unknown")) # 'Alpha'
print(decode("Z", "A", "Alpha", "B", "Beta", "Fallback")) # 'Fallback'

# Remove multiple if-elif tests - Clean and easy to read
status_code = None
customer_status = decode(
    status_code,
    "A", "Active",
    "B", "Blocked",
    "C", "Closed",
    None, "Unknown",
    default="Other"
)

# Bloated without decode...
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

```
---

## 🔹 NONEIF
```python
from pynvl import noneif

print(noneif(5, 5))   # None
print(noneif(7, 8))   # 7
```
---

## 🔹 NVL2
```python
from pynvl import nvl2

print(nvl2("X", "not-null", "is-null"))  # 'not-null'
print(nvl2(None, "not-null", "is-null")) # 'is-null'
```
---

## 📊 Pandas Integration

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

