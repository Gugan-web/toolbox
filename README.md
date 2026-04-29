# 🧰 My Instant Toolbox (Advanced v0.2.5)

[![PyPI version](https://img.shields.io/pypi/v/my-instant-toolbox.svg?v=0.2.5)](https://pypi.org/project/my-instant-toolbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**My Instant Toolbox** is a professional-grade CLI automation suite. Version 0.2.5 introduces a live system dashboard, regex search-replace, incremental backups, and a suite of diagnostic tools.

---

## ✨ v0.2.5 Highlights

| Feature | Description |
| :--- | :--- |
| **Live Dashboard** | Real-time monitoring of CPU (per-core), RAM, Network, and Processes. |
| **Recursive Organizer** | Sort deep directory structures with a dry-run preview. |
| **Advanced Renamer** | Case conversion (snake/kebab), numbering, and preview confirmation. |
| **Incremental Backups** | Save space by only backing up changed files since the last run. |
| **Regex Find-Replace** | Power-user search and replace with colorized diff previews. |
| **Hash Checker** | Verify file integrity with SHA256, MD5, and Blake2b. |
| **Text Analysis** | Word frequency, line counts, and unique word analytics. |
| **Env Doctor** | Diagnose your local Python environment and dependency health. |

---

## 🚀 Installation

```bash
pip install my-instant-toolbox --upgrade
```

---

## 🛠️ Advanced Usage Guide

### 📂 Organization & Renaming
```bash
# Organize a directory and its subdirectories (Dry Run)
toolbox organize ./my_project --recursive --dry-run

# Convert filenames to snake_case and add numbering
toolbox rename ./images --case snake --number
```

### 🔒 Security & Forensics
```bash
# Calculate a SHA256 hash
toolbox hash script.py --algo sha256

# Verify a file against a known hash
toolbox hash backup.zip --verify 5d41402abc4b2a76b9719d911017c592
```

### 📊 System & Environment
```bash
# Launch the LIVE refresh Resource Dashboard
toolbox sysinfo --live

# Check your development environment
toolbox doctor
```

### 📝 Content Analysis
```bash
# See top 10 most used words in a document
toolbox text README.md --top 10
```

---

## 📑 Changelog (v0.2.5)
- **New Command**: `hash` for checksum verification.
- **New Command**: `text` for file statistics and frequency analysis.
- **New Command**: `doctor` for environment health checks.
- **Improved**: `sysinfo` now features a `--live` mode with per-core CPU and top processes.
- **Improved**: `backup` supports `--incremental` mode and custom exclusions.
- **Improved**: `find-replace` now supports `--regex` and `--ignore-case`.
- **UX**: Added ASCII banner, version flag, and beautiful Rich progress bars.

---

## 📜 License
This project is licensed under the **MIT License**.

---
*Built with Rich, Typer, and ❤️ for the Automation community.*
