# Tasks: py-token-usage-reducer

## Task 1: Dependencies und Projektumgebung

- [x] Dependencies installieren: `pypdf`, `python-docx`, `beautifulsoup4`, `tiktoken` via `uv add`
- [x] Acceptance: `pyproject.toml` und `uv.lock` sind aktualisiert, alle Pakete importierbar
- [x] Verify: `uv run python -c "import pypdf, docx, bs4, tiktoken; print('OK')"`
- [x] Files: `pyproject.toml`

## Task 2: Core-Infrastruktur (Tokenizer, Gitignore, TextUtils)

- [x] Core-Module implementieren:
  - `src/core/tokenizer.py`: BPE tiktoken Schätzung mit heurischtischem Fallback (~4 chars/token).
  - `src/core/gitignore.py`: Parser für `.gitignore`-Muster und Standard-Ignorierlisten (`.git`, `node_modules`, etc.).
  - `src/core/text_utils.py`: Normalisierung von Whitespace, Entfernung von HTML/Base64-Artefakten, Markdown-Optimierung.
- [x] Acceptance: Token-Berechnung liefert konsistente Werte; Verzeichnisfilterung ignoriert `.git` und `.gitignore`-Einträge.
- [x] Verify: `uv run pytest tests/test_core.py`
- [x] Files: `src/core/tokenizer.py`, `src/core/gitignore.py`, `src/core/text_utils.py`, `tests/test_core.py`

## Checkpoint 1: Core Services

- [x] Alle Core-Tests grün, ruff ohne Beanstandungen.

## Task 3: Markdown-Konverter (PDF, DOCX, HTML, IPYNB)

- [x] `src/modules/converter.py` erstellen mit Konvertern:
  - `convert_pdf_to_markdown`: Text- und Tabellenextraktion via `pypdf`.
  - `convert_docx_to_markdown`: Paragraphen, Headings, Tabellen via `python-docx`.
  - `convert_html_to_markdown`: BeautifulSoup-Parser, Strippen von Script/Style/Nav/Footer.
  - `convert_ipynb_to_markdown`: JSON-Parser, Code- & Markdown-Zellen sauber formatiert, Outputs optional filterbar.
- [x] Acceptance: Alle 4 Formate erzeugen sauberes, binärfreies Markdown.
- [x] Verify: `uv run pytest tests/test_converter.py`
- [x] Files: `src/modules/converter.py`, `tests/test_converter.py`

## Task 4: Python AST Code-Skelettierer

- [x] `src/modules/skeletonizer.py` implementieren:
  - Python AST `NodeTransformer` zur Beibehaltung von `def`, `class`, Typannotationen, Decorators und Docstrings.
  - Ersetzt Anweisungsrümpfe durch `...` (Ellipsis) oder `pass`.
  - Berechnet Vorher-/Nachher-Token-Ersparnis.
- [x] Acceptance: Valider Python-Code wird erzeugt, Rumpf-Logik entfernt, >60 % Token-Ersparnis.
- [x] Verify: `uv run pytest tests/test_skeletonizer.py`
- [x] Files: `src/modules/skeletonizer.py`, `tests/test_skeletonizer.py`

## Task 5: Projekt- & Architektur-Reporter

- [x] `src/modules/reporter.py` implementieren:
  - Traversiert Verzeichnisse unter Beachtung von `.gitignore`.
  - Erstellt strukturierte Dateibaum-Übersicht mit Größen- und Tokenangaben.
  - Extrahiert Top-Imports und Modul-Beziehungen.
  - Identifiziert die "Top Token Consumers".
- [x] Acceptance: Kompakter Markdown-Report für beliebige Projektordner wird generiert.
- [x] Verify: `uv run pytest tests/test_reporter.py`
- [x] Files: `src/modules/reporter.py`, `tests/test_reporter.py`

## Checkpoint 2: Reducer Engines 1

- [x] Konverter, Skelettierer und Reporter sind vollständig getestet.

## Task 6: Data & Schema Reducer (JSON, CSV, SQL)

- [x] `src/modules/data_reducer.py` implementieren:
  - JSON: Erkennung von Objekt- und Listenstrukturen, Typ-Inferenz, 2-3 Beispieldatensätze.
  - CSV: Spaltenüberschriften, Datentypen, 2-3 Beispielzeilen.
  - SQL: Extraktion von `CREATE TABLE`-Statements und Schema-Informationen, Filterung riesiger `INSERT INTO`-Datenblöcke.
- [x] Acceptance: Riesige Datensätze schrumpfen auf wenige Zeilen Schema + Sample zusammen.
- [x] Verify: `uv run pytest tests/test_data_reducer.py`
- [x] Files: `src/modules/data_reducer.py`, `tests/test_data_reducer.py`

## Task 7: Log & Stacktrace Compressor

- [x] `src/modules/log_compressor.py` implementieren:
  - Entfernt ANSI-Farbcodes und Terminal-Steuerzeichen.
  - Faltet wiederkehrende Framework-Frames (z. B. aus virtualenv/site-packages) zusammen.
  - Isoliert Root-Cause-Exception und relevante App-Codezeilen.
- [x] Acceptance: Typische 500-Zeilen-Logs schrumpfen auf <30 Zeilen relevante Diagnoseinfos.
- [x] Verify: `uv run pytest tests/test_log_compressor.py`
- [x] Files: `src/modules/log_compressor.py`, `tests/test_log_compressor.py`

## Task 8: Import Dependency Tracer & Git Diff Packager

- [x] `src/modules/dep_tracer.py`: Analysiert rekursiv lokale Imports ausgehend von einer Einstiegsdatei und bündelt nur abhängige Dateien.
- [x] `src/modules/diff_packager.py`: Führt `git diff` aus und hängt die Skelette der geänderten Dateien an.
- [x] Acceptance: Minimalistischer Kontext für gezielte Feature-Arbeit und Code-Reviews.
- [x] Verify: `uv run pytest tests/test_dep_tracer.py tests/test_diff_packager.py`
- [x] Files: `src/modules/dep_tracer.py`, `src/modules/diff_packager.py`, `tests/test_dep_tracer.py`, `tests/test_diff_packager.py`

## Checkpoint 3: Alle Reducer Engines fertig

- [x] Alle 7 Reducer-Module sind unit-getestet.

## Task 9: In-Depth Documentation & Manual Engine

- [x] `src/docs/manual.py` implementieren:
  - Detaillierte Beschreibungen für jedes Tool.
  - "Wann nützlich?" (Praxisszenarien und typische Tokenfallen).
  - "Wie ausführen?" (CLI-Syntax, Flags, GUI-Anleitung).
  - Erwartete Token-Ersparnis.
- [x] Acceptance: Zentrales Handbuch steht für CLI `guide`-Befehl und GUI Hilfe-Tab zur Verfügung.
- [x] Verify: `uv run python -c "from src.docs.manual import get_full_manual; print(len(get_full_manual()))"`
- [x] Files: `src/docs/manual.py`

## Task 10: Unified CLI Dispatcher & Subcommands

- [x] `src/cli/parser.py` implementieren:
  - Subcommands: `convert`, `report`, `skeleton`, `schema`, `compress-log`, `trace-deps`, `diff-pack`, `guide`.
  - Globale Flags: `-o` / `--output`, `--gui`, `-v` / `--verbose`.
- [x] `src/main.py` als Dispatcher aktualisieren.
- [x] Acceptance: Alle Subcommands funktionieren per CLI, inklusive `--help` und `guide [tool]`.
- [x] Verify: `uv run pytest tests/test_cli.py`
- [x] Files: `src/cli/parser.py`, `src/main.py`, `tests/test_cli.py`

## Checkpoint 4: CLI vollständig einsatzbereit

- [x] CLI-Befehle funktionieren in der Shell.

## Task 11: GUI Basisarchitektur & Styling

- [x] PySide6 Basisoberfläche:
  - `src/gui/theme.py`: Modernes Dark- und Light-Theme mit CSS/QSS, hoher Kontrast.
  - `src/gui/workers.py`: Generischer `TaskWorker` mit Signals für finished und error.
  - `src/gui/app.py`: Hauptfenster mit TabWidget, F11 Vollbild-Umschaltung, QSettings-Persistenz (Größe, Position, Theme).
- [x] Acceptance: GUI startet responsiv im Fenster- und Vollbildmodus, Theme-Wechsel funktioniert.
- [x] Verify: `uv run pytest tests/test_gui.py`
- [x] Files: `src/gui/theme.py`, `src/gui/workers.py`, `src/gui/app.py`

## Task 12: Tool-Tabs & Interaktiver Hilfe-Tab

- [x] GUI-Tabs implementieren (`src/gui/tabs/`):
  - `converter_tab.py`: Drag&Drop/Dateiauswahl, Konvertierungs-Vorschau, Token-Vergleich.
  - `reporter_tab.py`: Ordnerauswahl, Checkboxen für AST-Skelette, Live-Report-Ansicht.
  - `skeletonizer_tab.py`: Code-Eingabe / Dateiauswahl, Nebeneinander-Ansicht, Ersparnis-Zähler.
  - `data_reducer_tab.py`: JSON/CSV/SQL Eingabe & Schema-Vorschau.
  - `log_compressor_tab.py`: Log-Textfeld, Bereinigungs-Button, Vorher/Nachher-Statistik.
  - `context_packager_tab.py`: Import-Tracer & Git-Diff Packer.
  - `token_inspector_tab.py`: Direkte Token-Zählung beliebiger Texte / Dateien mit Modell-Limits (32k, 128k, 200k).
  - `help_tab.py`: Vollwertiges, durchsuchbares Benutzerhandbuch mit Anleitungen und CLI-Befehlen.
- [x] Copy-to-Clipboard und Speichern-Buttons in allen Tabs.
- [x] Acceptance: Alle Tabs sind voll funktionsfähig und frieren die GUI dank Worker-Threads niemals ein.
- [x] Files: `src/gui/tabs/*.py`

## Checkpoint 5: Vollständige Desktop-Funktionalität

- [x] Alle Tabs und Features in der Desktop-GUI getestet und funktionstüchtig.

## Task 13: Ausführliche README.md

- [x] `README.md` komplett überarbeiten:
  - Motivation & Token-Ersparnis für Coding-Agenten.
  - Schnellstart & Installation via `uv`.
  - Ausführlicher Werkzeugkatalog (Wann nützlich?, CLI-Befehle, GUI-Anleitung, Ersparnis).
  - Dokumentation von GUI-Tastenkombinationen (F11, Strg+Q, Themes).
- [x] Acceptance: `README.md` ist für neue Entwickler sofort verständlich und vollständig.
- [x] Files: `README.md`

## Task 14: End-to-End Qualitätssicherung & Finalisierung

- [x] Gesamte Testsuite durchlaufen (`uv run pytest -v`).
- [x] Ruff Linter & Formatter (`uv run ruff check .`, `uv run ruff format .`).
- [x] End-to-End Smoke Test aller CLI-Befehle.
- [x] Acceptance: 100 % Tests grün, 0 Linting-Fehler.
- [x] Files: Alle
