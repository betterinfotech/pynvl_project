# 🗺️ Roadmap

The `pynvl` package is just getting started.  
Here are the planned enhancements and future directions.

---

## 🔹 Core Functions
- Initial helpers: `nvl`, `decode`, `sign`
-  Add more PL/SQL-inspired helpers:
- `extract`, `extract_xml`

---

## 🔹 Pandas Integration
- `pd_nvl(series, default)` => fill `NaN`/`None` with default  
- `pd_decode(series, mapping, default)` =>map values with fallback  
- `pd_sign(series)` => vectorized numeric sign  

---

## 🔹 Regex Helpers (TO DO)
- `regexp_like(string, pattern)` => boolean match  
- `regexp_substr(string, pattern, occurrence=1)` => extract substring  
- `regexp_replace(string, pattern, replacement)` => regex substitution  
- `regexp_instr(string, pattern)` => position of match

## 🔹 Testing & Quality
- Expand test coverage across all functions  
- Cover edge cases (e.g. `None == None` in `decode`)  

---

## 🔹 Documentation
- Expand API docs with detailed examples  
- Tutorials for analysts and data engineers transitioning from SQL  

---

## 🔹 Longer-Term Ideas
- Performance optimizations for large data sets  


---

💡 Contributions and ideas are welcome! See [CONTRIBUTING.md](contributing.md)
 for guidelines.
