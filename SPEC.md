# Specification: py-token-usage-reducer

## 1. Objective

Entwicklung einer modularen, datenschutzfreundlichen und 100 % lokalen Desktop- und Kommandozeilen-Anwendung (`py-token-usage-reducer`), die Entwicklern hilft, den Tokenverbrauch bei der Arbeit mit KI-Coding-Agenten drastisch zu reduzieren.
Die Software bietet Konverter, Filter, Skelettierer und Analyse-Werkzeuge, um Dokumente, Codebasen und Fehlerdaten vor der Übergabe an LLMs deterministisch einzudampfen. Sowohl im Programm selbst als auch in der `README.md` steht eine ausführliche, leicht verständliche Dokumentation zur Verfügung.

---

## 2. Capability Map & Modul-Architektur

| Modul-ID | Name | Verantwortung | Abhängigkeiten |
| --- | --- | --- | --- |
| `core` | Core Engine & Utilities | Token-Zählung (tiktoken & Heuristik), Datei-I/O, Textbereinigung, .gitignore-Filter | — |
| `converter` | Markdown Converter | Konvertiert PDF, DOCX, HTML und IPYNB in minimales, strukturiertes Markdown | `core` |
| `reporter` | Project Architecture Reporter | Generiert kompakte Codebase-Übersichten: Dateibaum, Modul-Abhängigkeiten, Metriken | `core` |
| `skeletonizer` | Code Skeletonizer | AST-basierte Extraktion von Python-Klassen, Methoden, Signaturen und Docstrings (ohne Rümpfe) | `core` |
| `data-reducer` | Data & Schema Reducer | Reduziert JSON, CSV und SQL Dumps auf Daten-Schema + 2-3 Beispieldatenzeilen | `core` |
| `log-compressor` | Log & Stacktrace Compressor | Bereinigt ANSI-Codes, filtert Framework-Frames, isoliert Fehlerursache | `core` |
| `dep-tracer` | Dependency Context Collector | Findet ausgehend von einer Einstiegsdatei den lokalen Import-Graphen und bündelt relevanten Code | `core` |
| `diff-packager` | Git Diff Context Packager | Bündelt Git-Diffs (Working Tree / Staged) mit den Signaturen der betroffenen Dateien | `core`, `skeletonizer` |
| `docs-engine` | Verbose Help & Manual | Liefert detaillierte Hilfetexte, Syntax, Best Practices und CLI-Guides (für CLI, GUI und README) | `core` |
| `cli` | Command-Line Interface | Subcommands für jedes Tool, standardisierte Flags, interaktiver Guide | Alle Module |
| `gui` | PySide6 Desktop GUI | Tab-basiertes UI mit Live-Vorschau, Zwischenablage, Dark/Light Theme, Vollbild (F11), Persistenz | Alle Module |

---

## 3. Tech Stack & Abhängigkeiten

- **Sprache**: Python >= 3.11 (Ziel: moderne Python 3.12+ Typisierung)
- **Paketmanager**: `uv`
- **GUI Framework**: `PySide6` (Qt 6)
- **Dokument-Parsing**:
  - `pypdf` (Pure Python PDF-Parser)
  - `python-docx` (DOCX-Parser)
  - `beautifulsoup4` (HTML-Parser via Standard `html.parser`)
  - Jupyter Notebooks (`.ipynb`): Standardbibliothek `json`
- **Token Estimation**: `tiktoken` (mit automatischer Heuristik-Fallback-Funktion bei Offline-/Fehlersituationen)
- **CLI**: Standardbibliothek `argparse` (minimalistisch, stabil, keine unnötigen Abhängigkeiten gem. Ponytail-Prinzip)
- **Linter & Formatter**: `ruff`
- **Testing**: `pytest`

---

## 4. Commands

```bash
# Abhängigkeiten synchronisieren
uv sync

# CLI Ausführung
uv run py-token-usage-reducer --help
uv run py-token-usage-reducer convert input.pdf -o output.md
uv run py-token-usage-reducer report ./my-project -o PROJECT_SUMMARY.md
uv run py-token-usage-reducer skeleton src/main.py
uv run py-token-usage-reducer schema data.json
uv run py-token-usage-reducer compress-log error.log
uv run py-token-usage-reducer trace-deps src/main.py
uv run py-token-usage-reducer diff-pack
uv run py-token-usage-reducer guide [tool-name]

# GUI starten
uv run py-token-usage-reducer --gui
# oder direkt das Skript:
uv run main

# Tests & Qualitätssicherung
uv run pytest
uv run ruff check .
uv run ruff format . --check
```

---

## 5. Projektstruktur

```text
py-token-usage-reducer/
├── SPEC.md
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py                    # Haupteinstiegspunkt (CLI / GUI Dispatcher)
│   ├── core/                      # Zentrale Basisfunktionen
│   │   ├── __init__.py
│   │   ├── tokenizer.py           # Token-Zählung (tiktoken & Fallback)
│   │   ├── gitignore.py           # .gitignore-Filterung für Verzeichnisse
│   │   └── text_utils.py          # Markdown-Bereinigung, Whitespace-Trimming
│   ├── modules/                   # Die spezifischen Reduktions-Tools
│   │   ├── __init__.py
│   │   ├── converter.py           # PDF, DOCX, HTML, IPYNB -> Markdown
│   │   ├── reporter.py            # Codebase- & Architektur-Report
│   │   ├── skeletonizer.py        # Python AST-Skelettierer (Signatures only)
│   │   ├── data_reducer.py        # JSON, CSV, SQL Schema-Extraktion
│   │   ├── log_compressor.py      # Log- & Stacktrace-Kompression
│   │   ├── dep_tracer.py          # Lokaler AST-Import-Tracer
│   │   └── diff_packager.py       # Git Diff + Schnittstellen-Packer
│   ├── docs/                      # Detaillierte Hilfetexte & Anleitungen
│   │   ├── __init__.py
│   │   └── manual.py              # Strukturierte Texte für GUI, CLI & Export
│   ├── cli/                       # Kommandozeilenschnittstelle
│   │   ├── __init__.py
│   │   └── parser.py              # argparse-Subcommands & Guide
│   └── gui/                       # PySide6 Desktop-Oberfläche
│       ├── __init__.py
│       ├── app.py                 # Hauptfenster, F11 Vollbild, QSettings
│       ├── theme.py               # Dark & Light Themes (QSS)
│       ├── workers.py             # QThread/Worker für asynchrone Berechnungen
│       └── tabs/                  # Einzelne Tool-Ansichten
│           ├── __init__.py
│           ├── converter_tab.py
│           ├── reporter_tab.py
│           ├── skeletonizer_tab.py
│           ├── data_reducer_tab.py
│           ├── log_compressor_tab.py
│           ├── dep_tracer_tab.py
│           ├── diff_packager_tab.py
│           ├── token_inspector_tab.py
│           └── help_tab.py        # In-App Handbuch & Quickstart
└── tests/                         # Pytest-Testsuite
    ├── __init__.py
    ├── test_tokenizer.py
    ├── test_converter.py
    ├── test_reporter.py
    ├── test_skeletonizer.py
    ├── test_data_reducer.py
    ├── test_log_compressor.py
    ├── test_dep_tracer.py
    ├── test_diff_packager.py
    └── test_cli.py
```

---

## 6. Code Style & Konventionen

- Quellcode-Kommentare, Docstrings, Klassen- und Variablennamen auf **Englisch**.
- Nutzeroberfläche (GUI-Labels, Tooltips, Fehlermeldungen, CLI-Hilfetexte) auf **Deutsch**.
- Strikte Typisierung (`list[Path]`, `str | None`, `dict[str, Any]`).
- Vermeidung überflüssiger Abstraktionen: Direkte, performante Standard-Python-Funktionen.
- Beispiel:

```python
def extract_python_skeleton(source_code: str) -> str:
    """Extract signatures, class declarations, and docstrings from Python source.

    Strips function and method bodies to save tokens while retaining the public API.
    """
    ...
```

---

## 7. Testing-Strategie

- Unit-Tests für jedes Modul in `tests/test_*.py` mit `pytest`.
- Schnelle Tests mit synthetischen Daten (Beispiel-PDFs/DOCX via Fixtures generiert oder In-Memory getestet).
- AST-Tests verifizieren, dass Docstrings und Signaturen erhalten bleiben, während Rumpf-Anweisungen (wie Berechnungen und `return ...`) durch `...` (Ellipsis) ersetzt werden.
- CLI-Subcommands werden auf Exit-Codes und korrekte Ausgaben getestet.

---

## 8. Boundaries

- **Always**:
  - `.gitignore` und Standard-Ausschlussmuster (`.git`, `node_modules`, `__pycache__`, `.venv`, `.env`) beim Scannen von Verzeichnissen respektieren.
  - Operationen in der GUI über Worker-Threads (`QThread`) ausführen, damit die Oberfläche flüssig bleibt.
  - Sowohl Fenstermodus als auch Vollbildmodus (Taste `F11`) in der PySide6-GUI unterstützen.
  - Fensterabmessungen und Theme-Einstellungen persistent via `QSettings` speichern.
- **Ask First**:
  - Hinzufügen weiterer schwergewichtiger Drittanbieter-Bibliotheken.
  - Änderungen am Kern-CLI-Befehlsformat.
- **Never**:
  - Externe Cloud-APIs kontaktieren oder Netzwerk-Verbindungen aufbauen.
  - Dateiinhalte ohne expliziten Nutzerbefehl überschreiben.

---

## 9. Success Criteria

1. **Dokumenten-Konvertierung**: PDF, DOCX, HTML und IPYNB werden in sauberes, schlankes Markdown ohne Binärdaten überführt.
2. **Projekt-Report**: Ein kompletter Projektordner wird analysiert und in eine strukturierte Übersicht (Dateibaum, Dateigrößen, geschätzte Tokens, Haupt-Imports) exportiert.
3. **AST-Skelettierer**: Python-Dateien werden auf ihre Signaturen und Docstrings reduziert (Reduktion typischerweise > 60-80 % der Tokens).
4. **Data-Reducer**: Grosse JSON/CSV/SQL-Dumps werden in das Tabellenschema + wenige Beispieldatensätze konvertiert.
5. **Log-Kompression**: Rauschen aus Tracebacks und Logs wird entfernt, die Fehlermeldung und relevante Codezeilen bleiben erhalten.
6. **GUI & CLI Parität**: Alle Funktionen lassen sich sowohl über die CLI als auch über die PySide6-GUI mit Copy-to-Clipboard bedienen.
7. **Ausführliche Hilfe**: Umfassender `guide`-Befehl in der CLI, durchsuchbarer Hilfe-Tab in der GUI sowie eine vollständige `README.md` mit konkreten Praxisbeispielen.
