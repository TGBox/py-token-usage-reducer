# py-token-usage-reducer

A python program providing tools to reduce your token usage when working with coding agents.

## Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

- Qt 6 (wird automatisch über uv installiert)


## Setup & Ausführung

```bash
uv sync

# GUI starten
uv run main
# oder:
uv run py-token-usage-reducer

# Tests ausführen
uv run test

# Standalone-Exe mit PyInstaller bauen
uv run build
```

## Framework

Dieses Projekt verwendet **PySide6**.

## Projektstruktur

```
py-token-usage-reducer/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── build.py
│   └── tools.py
├── tests/
│   └── test_main.py
├── pyproject.toml
└── README.md
```