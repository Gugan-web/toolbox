# 🧰 My Instant Toolbox

[![PyPI version](https://img.shields.io/pypi/v/my-instant-toolbox.svg)](https://pypi.org/project/my-instant-toolbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/my-instant-toolbox.svg)](https://pypi.org/project/my-instant-toolbox/)

**My Instant Toolbox** is a modern, high-performance CLI suite designed to streamline common automation tasks and system monitoring. Built with Python, it provides a unified interface for file management, directory security, and real-time system performance insights.

---

## ✨ Key Features

| Tool | Description |
| :--- | :--- |
| **File Organization** | Intelligently sorts cluttered directories by file extension. |
| **Bulk Renaming** | Powerful pattern-based renaming with prefix/suffix/replace support. |
| **Secure Backups** | Instant, timestamped ZIP compression for critical directories. |
| **Global Find & Replace** | Mass find-and-replace across multiple files with glob filtering. |
| **System Insights** | Real-time monitoring dashboard for CPU, RAM, and Disk metrics. |
| **DevOps Automation** | Built-in publishing workflow for package maintenance. |

---

## 🚀 Installation

### Global Installation
Install the toolbox directly from PyPI:
```bash
pip install my-instant-toolbox
```

### Local Development
To set up for local development or custom modifications:
```bash
git clone https://github.com/your-username/my-instant-toolbox.git
cd my-instant-toolbox
pip install -e .
```

---

## 🛠️ Usage Guide

Once installed, use the `toolbox` entry point to access the commands.

### 📁 File Management
```bash
# Organize a directory by file types
toolbox organize ./downloads

# Bulk rename files (e.g., replace 'IMG' with 'vacation')
toolbox rename ./images --replace "IMG" --replacement "vacation"
```

### 🔒 Security & Maintenance
```bash
# Create a backup of your project
toolbox backup ./source_code --destination ./backups

# Mass update code or configuration
toolbox find-replace ./config "localhost" "192.168.1.1" --pattern "*.yaml"
```

### 📊 System Monitoring
```bash
# Launch the resource dashboard
toolbox sysinfo
```

---

## 👩‍💻 Developer Workflow

This toolbox is designed to be extensible. We've included automation for contributors to maintain the package.

### Publishing to PyPI
Ensure your version is updated in `pyproject.toml` and your `.pypirc` is configured, then run:
```bash
# Test the build process
toolbox publish --dry-run

# Build and upload to PyPI
toolbox publish
```

---

## 📜 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
*Developed with ❤️ for the Python Automation Community.*
