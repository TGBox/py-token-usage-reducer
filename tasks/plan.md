# Implementation Plan: py-token-usage-reducer

## Overview

Realisierung eines modularen, datenschutzkonformen Werkzeugsatzes (`py-token-usage-reducer`) zur Reduzierung des Tokenverbrauchs bei der Arbeit mit KI-Coding-Agenten. Das Tool bietet sowohl eine leistungsfähige CLI mit Subcommands als auch eine moderne PySide6 Desktop-GUI mit Fenster-/Vollbildmodus (F11), Dark/Light-Theme und interaktiver Hilfe.

## Architecture Decisions

1. **Zero External LLM APIs**: Vollständig lokale Ausführung über Python-Parser (AST, `pypdf`, `python-docx`, `beautifulsoup4`, JSON/CSV/SQL-Heuristiken).
2. **Minimal Dependencies (Ponytail-Prinzip)**: Einsatz bewährter, ressourcenschonender Bibliotheken (`pypdf`, `python-docx`, `beautifulsoup4`, `tiktoken`). Für CLI wird das standardmäßige `argparse` genutzt.
3. **Klare Trennung Logik vs. UI**: Alle Reduktionsfunktionen leben als reine, seiteneffektfreie Python-Module in `src/modules/` und `src/core/`. Sie sind zu 100 % unabhängig von PySide6 testbar.
4. **Asynchrone GUI-Ausführung**: Zeitaufwändige Aufgaben (z. B. Scannen großer Ordner oder Parsen dicker PDFs) laufen in `QThread`-Workern mit Qt-Signals.
5. **Persistenz & Ergonomie**: Fensterzustand, Geometrie und gewähltes Farbschema werden via `QSettings` gespeichert.

## Task List

### Phase 1: Foundation & Core Services

- [ ] Task 1: Abhängigkeiten und Projektkonfiguration einrichten (`uv add pypdf python-docx beautifulsoup4 tiktoken`)
- [ ] Task 2: Core-Infrastruktur implementieren (`src/core/tokenizer.py`, `src/core/gitignore.py`, `src/core/text_utils.py`) mit Tests

### Checkpoint 1: Core Services

- [ ] Alle Core-Tests laufen fehlerfrei durch (`uv run pytest tests/test_tokenizer.py tests/test_core.py`)

### Phase 2: Core Reducer Engines

- [ ] Task 3: Dokumenten-zu-Markdown-Konverter (`src/modules/converter.py` für PDF, DOCX, HTML, IPYNB) + Tests
- [ ] Task 4: Python AST Code-Skelettierer (`src/modules/skeletonizer.py`) + Tests
- [ ] Task 5: Projekt- & Architektur-Reporter (`src/modules/reporter.py`) + Tests

### Checkpoint 2: Reducer Engines

- [ ] Konverter, Skelettierer und Reporter sind vollständig unit-getestet und ruff-konform

### Phase 3: Specialized Data & Diagnostics Reducers

- [ ] Task 6: Data & Schema Reducer für JSON, CSV und SQL (`src/modules/data_reducer.py`) + Tests
- [ ] Task 7: Log & Stacktrace Compressor (`src/modules/log_compressor.py`) + Tests
- [ ] Task 8: Import Dependency Tracer (`src/modules/dep_tracer.py`) und Git Diff Packager (`src/modules/diff_packager.py`) + Tests

### Checkpoint 3: All Engines Complete

- [ ] Vollständige Testabdeckung aller 7 Reduktions-Engines

### Phase 4: Verbose Help System & CLI

- [ ] Task 9: Verbose Help & Manual Engine (`src/docs/manual.py`) mit ausführlichen Erklärungen, Wann-nutzen-Anleitungen und Beispielen
- [ ] Task 10: Unified CLI Dispatcher & Subcommands (`src/cli/parser.py`, `src/main.py`) + CLI-Tests

### Checkpoint 4: CLI Operability

- [ ] Alle CLI-Befehle (`convert`, `report`, `skeleton`, `schema`, `compress-log`, `trace-deps`, `diff-pack`, `guide`) funktionieren in der Konsole

### Phase 5: PySide6 Desktop GUI

- [ ] Task 11: GUI-Basisarchitektur (`src/gui/theme.py`, `src/gui/workers.py`, `src/gui/app.py`) mit F11 Vollbild, Dark/Light Mode, QSettings
- [ ] Task 12: Tool-Tabs und interaktiver Hilfe-Tab (`src/gui/tabs/`) mit Vorschau, Copy-to-Clipboard und Datei-Export

### Checkpoint 5: GUI Responsiveness

- [ ] Desktop-GUI startet reibungslos im Fenster- und Vollbildmodus, alle Tabs funktionieren ohne GUI-Freezes

### Phase 6: Exhaustive Documentation & Release Polish

- [ ] Task 13: Ausführliche `README.md` mit Schnellstart, Feature-Katalog, Use-Cases und Token-Ersparnis-Tipps
- [ ] Task 14: Gesamtprüfung (`pytest`, `ruff check`, `ruff format`, End-to-End-Funktionstest)

## Risks and Mitigations

| Risiko | Auswirkung | Mitigation |
| --- | --- | --- |
| Komplexe PDF-Layouts erzeugen unleserliches Markdown | Mittel | Robuste Extraktion via `pypdf`, Tabellen/Absatz-Normalisierung in `text_utils.py` |
| Extrem große Projektordner überlasten Arbeitsspeicher | Mittel | Streaming / Iteratives Traversieren, Standard-Exclude-Listen (`.git`, `node_modules`, `.venv`) |
| GUI blockiert bei großen Dateien | Hoch | Strikte Auslagerung in `QThread`-Worker mit Fortschritts-Signal |
