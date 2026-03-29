<div align="center">

```
⠀⠀⠀⠀⠀⠀⠀⠠⡧⠀⠀⠄⠀⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡄⠀⠀⠀⢺⠂⠀⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧
⠤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣿⠇⠀⢿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⠶⠶
⠀⠀⠘⢿⣿⣿⣟⠛⠛⠛⠛
⠀⠀⠁⠀⠈⠛⣿⣿⣦     ✧ combo hunter | a filter tool ✧
⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿            coded by t.me/vi77an
```

**combo hunter** · combo list filtering and cleaning tool

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey?style=flat-square)

</div>

---

## about

**combo hunter** is a Python command-line script for filtering and formatting large combo list files (`.txt`). It supports searching by domain, email, username, or URL, with a real-time progress bar and automatic parallel processing for large files.

---

## folder structure

```
project/
├── combo_hunter.py       ← main script
├── combos/               ← place your .txt files here for searching
├── limpar/               ← place your .txt files here for formatting
└── resultados/
    ├── dominios/         ← results from domain searches
    ├── emails/           ← results from email searches
    ├── usuarios/         ← results from username searches
    ├── urls/             ← results from URL searches
    └── limpos/           ← files formatted by clean mode
```

> All folders are created automatically when the script starts.

---

## requirements

- Python 3.8 or higher
- no external dependencies — standard library only

```bash
python --version   # should return 3.8+
```

---

## usage

```bash
python combo_hunter.py
```

The script opens an interactive menu with two modes:

### mode 1 — search

Filters lines from a `.txt` file by a search term. Four types available:

| type | description | match example |
|------|-------------|---------------|
| **domain** | domain/site field before the login | `netflix.com:user:pass` |
| **email** | full email address found in the line | `user@gmail.com:pass` |
| **username** | login/username field | `john123:password` |
| **url** | any occurrence of the term in the line | `https://netflix.com/...` |

Results are saved to `resultados/<type>/<term>@<count>_<date>.csv`.

### mode 2 — clean

Reformats files in the `url:login:password` pattern. Three output options:

| option | input | output |
|--------|-------|--------|
| `1` | `https://site.com:user:pass` | `user:pass` |
| `2` | any | keeps lines with URL, preserves others |
| `3` | any | keeps original unchanged |

---

## supported formats

The script automatically recognizes the following line formats:

```
https://site.com:login:password      ← url:login:password
http://site.com:login:password       ← url:login:password (http)
login:password                       ← log:pass
login@domain.com:password            ← email:pass
```

---

## performance

The script adapts its search strategy based on file size:

- **small files** (< 200,000 lines): linear search with progress bar
- **large files** (≥ 200,000 lines): parallel search using all available CPU cores (`multiprocessing.Pool`)

In both cases the progress bar updates in real time, showing match count, percentage, and elapsed time.

---

## output

Result files are saved as `.csv` with the following naming pattern:

```
<term>@<count>_<YYYYMMDD_HHMMSS>.csv
```

Example: `netflix@1523_20240315_142301.csv`

The first line of each file contains a credits comment. The remaining lines contain the matched entries, one per line.

---

## credits

developed with 🩷 by [vilanele](https://t.me/vi77an)
