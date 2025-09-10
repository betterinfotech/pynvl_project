# 🗺️ Roadmap

The `pynvl` package is just getting started.  
Here are the planned enhancements and future directions.

---

## 📦 Core Functions
- ✅ Initial helpers: `nvl`, `decode`, `sign`
- ➡️ Add more PL/SQL-inspired helpers:
  - `noneif`, `coalesce`, `nvl2`

---

## 📊 Pandas Integration
- 📌 `pd_nvl(series, default)` → fill `NaN`/`None` with default  
- 📌 `pd_decode(series, mapping, default)` → map values with fallback  
- 📌 `pd_sign(series)` → vectorized numeric sign  
- 📌 `pd_extract_date(series, field)` → year, month, quarter, etc.

---

## 🔍 Regex Helpers
- 🔎 `regexp_like(string, pattern)` → boolean match  
- 🔎 `regexp_substr(string, pattern, occurrence=1)` → extract substring  
- 🔎 `regexp_replace(string, pattern, replacement)` → regex substitution  
- 🔎 `regexp_instr(string, pattern)` → position of match

## 🧪 Testing & Quality
- 📈 Expand test coverage across all functions  
- ✅ Cover edge cases (e.g., `None == None` in `decode`)  
- 🛠️ Add property-based testing for robustness  

---

## 🌍 Documentation
- 📚 Expand API docs with detailed examples  
- 🌐 Publish full site via GitHub Pages (MkDocs Material)  
- 📝 Tutorials for analysts & data engineers transitioning from SQL  

---

## 🚀 Longer-Term Ideas
- 🧩 Compatibility layers for Spark DataFrames / Dask  
- ⚡ Performance optimizations for large data sets  
- 📦 Optional Cython/Rust backends for hot functions  

---

💡 Contributions and ideas are welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
