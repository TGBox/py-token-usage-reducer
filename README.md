# py-token-usage-reducer 🚀

> **Lokale Werkzeuge zur radikalen Reduzierung des Tokenverbrauchs bei der Arbeit mit KI-Coding-Agenten (Claude, GPT-4, Gemini & Co.).**

`py-token-usage-reducer` ist ein schlankes, modulares und 100 % lokales Open-Source-Werkzeug, das sowohl als **leistungsfähige Befehlszeilen-Anwendung (CLI)** als auch als **moderne Desktop-Oberfläche (PySide6)** betrieben werden kann.

Alle Bereinigungen, Konvertierungen und Analysen laufen **vollständig offline und deterministisch auf deinem Rechner**. Keine API-Keys, keine Drittanbieter-Netzwerkanfragen, keine laufenden Kosten und maximaler Quellcode-Datenschutz.

---

## Inhaltsverzeichnis

- [Warum Token-Reduktion?](#warum-token-reduktion)
- [Voraussetzungen & Installation](#voraussetzungen--installation)
- [Schnellstart](#schnellstart)
- [Werkzeug-Katalog (Ausführliches Handbuch)](#werkzeug-katalog-ausführliches-handbuch)
  - [1. Dokumenten-zu-Markdown-Konverter (`convert`)](#1-dokumenten-zu-markdown-konverter-convert)
  - [2. Projekt- & Architektur-Reporter (`report`)](#2-projekt---architektur-reporter-report)
  - [3. Python AST Code-Skelettierer (`skeleton`)](#3-python-ast-code-skelettierer-skeleton)
  - [4. Data & Schema Reducer (`schema`)](#4-data--schema-reducer-schema)
  - [5. Log & Stacktrace Compressor (`compress-log`)](#5-log--stacktrace-compressor-compress-log)
  - [6. Smart Dependency Context Collector (`trace-deps`)](#6-smart-dependency-context-collector-trace-deps)
  - [7. Git Diff Context Packager (`diff-pack`)](#7-git-diff-context-packager-diff-pack)
  - [8. Interaktives Handbuch & Hilfe (`guide`)](#8-interaktives-handbuch--hilfe-guide)
- [Desktop-GUI (PySide6)](#desktop-gui-pyside6)
- [Befehlszeilen-Übersicht (CLI-Referenz)](#befehlszeilen-übersicht-cli-referenz)
- [Entwicklung & Qualitätssicherung](#entwicklung--qualitätssicherung)

---

## Warum Token-Reduktion?

Beim Arbeiten mit KI-gestützten Coding-Agenten (wie GitHub Copilot Workspace, Claude Dev, Cursor, Aider oder Antigravity) treten typischerweise drei große Probleme auf:

1. **Kontextfenster-Überlauf**: PDFs, unbereinigtes HTML, riesige Datendumps oder komplette Repositories sprengen das Kontextfenster (oder verdrängen frühere Anweisungen).
2. **Qualitätsverlust (Lost in the Middle)**: Je mehr irrelevanter Ballast (CSS, Binärdaten, Framework-Tracebacks) im Prompt landet, desto schlechter und fehleranfälliger werden die Antworten des Modells.
3. **Kosten & Latenz**: Jedes übertragene Megabyte kostet echtes Geld und verlängert die Antwortzeit spürbar.

`py-token-usage-reducer` filtert diesen Ballast **vor** der Übergabe an den Agenten heraus.

---

## Voraussetzungen & Installation

- **Python**: 3.11 oder höher
- **Paketmanager**: [uv](https://docs.astral.sh/uv/) (empfohlen)

```bash
# Repository klonen
git clone https://github.com/DaniBani/py-token-usage-reducer.git
cd py-token-usage-reducer

# Abhängigkeiten installieren und synchronisieren
uv sync
```

---

## Schnellstart

### 1. Grafische Benutzeroberfläche (GUI) starten

```bash
uv run py-token-usage-reducer --gui
```

### 2. Schnelle CLI-Befehle

```bash
# PDF-Spezifikation in schlankes Markdown wandeln
uv run py-token-usage-reducer convert anforderung.pdf -o anforderung.md

# Kompakten Architektur-Report deines Projekts generieren
uv run py-token-usage-reducer report . -o PROJECT_OVERVIEW.md

# Python-Klasse auf Schnittstellen & Typen skelettieren
uv run py-token-usage-reducer skeleton src/main.py

# Riesigen JSON-Dump auf Schema und 2 Zeilen reduzieren
uv run py-token-usage-reducer schema fixtures.json -s 2

# Terminal-Fehlerlog von Farben und Framework-Müll bereinigen
uv run py-token-usage-reducer compress-log crash.log

# Ausführliche Hilfe zu einem beliebigen Werkzeug anzeigen
uv run py-token-usage-reducer guide report
```

---

## Werkzeug-Katalog (Ausführliches Handbuch)

### 1. Dokumenten-zu-Markdown-Konverter (`convert`)

- **Beschreibung**: Konvertiert PDF-, Word- (`.docx`), HTML- und Jupyter-Notebook-Dateien (`.ipynb`) in sauberes, strukturiertes Markdown ohne visuelle Binärdaten.
- **💡 Wann ist diese Funktion nützlich?**:
  - Wenn du dem Agenten Dokumentationen, Whitepaper oder Tutorials zur Verfügung stellen willst.
  - Wenn Webseiten-Dumps hunderte Script-Tags, Navigationsmenüs oder Base64-Grafiken enthalten, die den Prompt überfüllen.
  - Wenn Jupyter Notebooks mit riesigen Diagrammen und Print-Ausgaben den Kontext sprengen.
- **💻 CLI-Befehle**:

  ```bash
  # Standard-Ausgabe in der Konsole
  uv run py-token-usage-reducer convert spezifikation.pdf

  # Ausgabe in Markdown-Datei speichern
  uv run py-token-usage-reducer convert handbuch.docx -o handbuch.md

  # HTML bereinigen (entfernt automatisch <script>, <style>, <nav>, <footer>, base64-Bilder)
  uv run py-token-usage-reducer convert doku.html -o doku.md

  # Jupyter Notebook (Code-Ausgaben standardmäßig ausgelassen zur Token-Ersparnis)
  uv run py-token-usage-reducer convert analyse.ipynb -o analyse.md
  # Optional mit Code-Ausgaben:
  uv run py-token-usage-reducer convert analyse.ipynb --include-outputs
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `📄 Konverter` aufrufen.
  2. Datei auswählen oder per Drag & Drop hineinziehen.
  3. `In Markdown konvertieren` klicken und Ergebnis direkt in die Zwischenablage kopieren.

- **📉 Typische Token-Ersparnis**: **70 % bis 95 %** gegenüber Rohdaten.

---

### 2. Projekt- & Architektur-Reporter (`report`)

- **Beschreibung**: Durchsucht ein Repository unter Beachtung deiner `.gitignore`-Datei und erzeugt einen kompakten Überblick über Dateistruktur, Codezeilen, Token-Verbrauch, Abhängigkeiten und Komponenten.
- **💡 Wann ist diese Funktion nützlich?**:
  - Zu Beginn einer neuen Agenten-Session, um der KI das gesamte Projekt kompakt vorzustellen.
  - Bei großen Repositories (>10.000 Zeilen), bei denen es unbezahlbar wäre, alle Dateien zu übertragen.
  - Um die „Top-Token-Verbraucher“ (größte Dateien im Repo) zu entlarven.
- **💻 CLI-Befehle**:

  ```bash
  # Aktuelles Verzeichnis analysieren
  uv run py-token-usage-reducer report .

  # Als PROJECT_OVERVIEW.md speichern
  uv run py-token-usage-reducer report . -o PROJECT_OVERVIEW.md

  # Mit automatisch eingebetteten API-Skeletten der wichtigsten Python-Dateien
  uv run py-token-usage-reducer report . --skeletons --max-skeletons 5 -o PROJECT_OVERVIEW.md
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `🏗️ Architektur-Report` wählen.
  2. Projektordner auswählen.
  3. `Projekt analysieren` drücken.

- **📉 Typische Token-Ersparnis**: **90 % bis 99 %** gegenüber der Übergabe aller Quellcodedateien.

---

### 3. Python AST Code-Skelettierer (`skeleton`)

- **Beschreibung**: Parst Python-Dateien über den offiziellen Python Abstract Syntax Tree (AST), entfernt alle Anweisungsrümpfe und ersetzt sie durch `...` (Ellipsis). Behält Klassendefinitionen, Methoden, Parameter, Typ-Annotationen, Decorators und Docstrings vollständig bei.
- **💡 Wann ist diese Funktion nützlich?**:
  - Wenn der Agent eine Funktion schreiben soll, die bestehende Services oder Hilfsfunktionen aufruft, aber die Implementierungsdetails dieser Services nicht kennen muss.
  - Um dem Modell das Typ- und Methodengerüst großer Klassen (z. B. Datenbankmodelle, API-Clients) bereitzustellen.
- **💻 CLI-Befehle**:

  ```bash
  # Datei skelettieren
  uv run py-token-usage-reducer skeleton src/services/database.py

  # In Schnittstellen-Datei speichern
  uv run py-token-usage-reducer skeleton src/main.py -o main_interface.py

  # Maximale Kompression ohne Docstrings
  uv run py-token-usage-reducer skeleton src/api.py --no-docstrings
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `🦴 Code-Skelette` öffnen.
  2. Datei laden oder Python-Code direkt in die linke Spalte einfügen.
  3. `Code skelettieren` klicken. Links und rechts wird der Vorher-/Nachher-Vergleich angezeigt.

- **📉 Typische Token-Ersparnis**: **60 % bis 85 %** pro Python-Quelldatei.

---

### 4. Data & Schema Reducer (`schema`)

- **Beschreibung**: Extrahiert aus großen JSON-Payloads, CSV-Dateien und SQL-Dumps die exakte Datenstruktur sowie wenige repräsentative Stichprobenzeilen.
- **💡 Wann ist diese Funktion nützlich?**:
  - Wenn du dem Agenten eine Datenbanktabelle oder einen API-Response zeigen willst, damit er eine SQL-Query oder ein Pydantic-Modell baut.
  - Wenn eine JSON-Datei 10.000 Objekte enthält, der Agent aber nur wissen muss, welche Felder vorkommen.
  - Wenn SQL-Backups tausende `INSERT INTO`-Zeilen enthalten.
- **💻 CLI-Befehle**:

  ```bash
  # JSON-Array auf Schema und 3 Beispiele reduzieren
  uv run py-token-usage-reducer schema kunden.json

  # CSV mit benutzerdefinierter Stichprobenanzahl
  uv run py-token-usage-reducer schema daten.csv --samples 2 -o schema.md

  # SQL-Dump von bulk-INSERTs befreien
  uv run py-token-usage-reducer schema dump.sql -o schema.sql
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `📊 Schema-Reducer` aufrufen.
  2. Datei auswählen oder JSON/CSV/SQL in das Textfeld einfügen.
  3. `Auf Schema & Samples reduzieren` klicken.

- **📉 Typische Token-Ersparnis**: **90 % bis 99 %** bei Datensätzen.

---

### 5. Log & Stacktrace Compressor (`compress-log`)

- **Beschreibung**: Bereinigt unübersichtliche Terminal- und Log-Ausgaben: Entfernt ANSI-Farbcodes, faltet hunderte identische Polling-Zeilen zusammen und blendet interne Framework-Frames (`site-packages`, `node_modules`) aus.
- **💡 Wann ist diese Funktion nützlich?**:
  - Beim Debugging, wenn der Terminal-Output 500 Zeilen lang ist, aber nur die Root Cause und dein eigener Code relevant sind.
  - Verhindert, dass Coding-Agenten durch interne Framework-Dateien verwirrt werden.
- **💻 CLI-Befehle**:

  ```bash
  uv run py-token-usage-reducer compress-log crash.log -o clean_crash.md
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `📋 Log-Kompressor` wählen.
  2. Rohen Terminal-Fehlertext einfügen.
  3. `Log komprimieren & bereinigen` klicken.

- **📉 Typische Token-Ersparnis**: **75 % bis 90 %** bei Tracebacks und Terminal-Dumps.

---

### 6. Smart Dependency Context Collector (`trace-deps`)

- **Beschreibung**: Analysiert ausgehend von einer Python-Einstiegsdatei rekursiv alle lokalen Modul-Imports und bündelt exakt diesen Abhängigkeits-Teilbaum in einen sauberen Kontext-Block.
- **💡 Wann ist diese Funktion nützlich?**:
  - Wenn du an einem bestimmten Feature arbeitest und dem Agenten weder zu wenig (fehlende Funktionen) noch zu viel (gesamtes Repo) Kontext geben willst.
  - Chirurgisch präzise Prompts für isolierte Refactorings.
- **💻 CLI-Befehle**:

  ```bash
  # Einstiegsdatei analysieren und lokalen Import-Baum bündeln
  uv run py-token-usage-reducer trace-deps src/main.py

  # Mit benutzerdefinierter Rekursionstiefe und Ausgabedatei
  uv run py-token-usage-reducer trace-deps src/main.py --depth 2 -o context.md
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `📦 Kontext-Packer` aufrufen und Modus `Import-Tracer` wählen.
  2. Einstiegsdatei wählen und `Kontext-Paket generieren` klicken.

- **📉 Typische Token-Ersparnis**: **80 % bis 95 %** gegenüber dem blinden Kopieren ganzer Verzeichnisse.

---

### 7. Git Diff Context Packager (`diff-pack`)

- **Beschreibung**: Liest deine aktuellen ungespeicherten (`git diff`) oder vorgemerkten (`git diff --staged`) Änderungen aus und ergänzt sie automatisch um die Schnittstellen-Skelette der betroffenen Dateien.
- **💡 Wann ist diese Funktion nützlich?**:
  - Wenn du den Coding-Agenten um ein Code-Review oder um neue Unit-Tests für deine aktuellen Änderungen bittest.
  - Das Modell versteht sofort die umgebende Klasse, ohne dass du die gesamten Dateien übertragen musst.
- **💻 CLI-Befehle**:

  ```bash
  # Aktuelle ungespeicherte Änderungen bündeln
  uv run py-token-usage-reducer diff-pack

  # Nur gestagte Änderungen analysieren
  uv run py-token-usage-reducer diff-pack --staged -o pr_context.md
  ```

- **🖥️ GUI-Bedienung**:
  1. Tab `📦 Kontext-Packer` aufrufen und Modus `Git-Diff Packer` wählen.
  2. `Kontext-Paket generieren` klicken.

- **📉 Typische Token-Ersparnis**: Bis zu **90 %** bei fokussierten Diffs.

---

### 8. Interaktives Handbuch & Hilfe (`guide`)

- **Beschreibung**: Zeigt die vollständige Dokumentation und Syntax direkt in deinem Terminal oder im In-App-Hilfe-Tab an.
- **💻 CLI-Befehle**:

  ```bash
  # Vollständiges Handbuch im Terminal lesen
  uv run py-token-usage-reducer guide

  # Spezifische Hilfe zu einem Werkzeug aufrufen
  uv run py-token-usage-reducer guide convert
  uv run py-token-usage-reducer guide skeleton
  uv run py-token-usage-reducer guide schema
  ```

---

## Desktop-GUI (PySide6)

Die grafische Benutzeroberfläche wurde für ergonomisches, schnelles Arbeiten entwickelt:

- **Fenstermodus & Vollbildmodus**:
  - Drücke jederzeit die Taste **F11**, um nahtlos zwischen maximiertem Vollbild und Fensteransicht zu wechseln.
- **Dark & Light Mode**:
  - Wechsle über das Menü `Ansicht` zwischen dunklem und hellem Farbschema mit optimiertem Kontrast.
- **Zustandsspeicherung (QSettings)**:
  - Deine Fenstergröße, Position, Vollbildstatus und das gewählte Theme werden beim Beenden automatisch persistent gespeichert.
- **Asynchrone Worker-Threads**:
  - Große Dateien und Repositories werden im Hintergrund via `QThread` verarbeitet, sodass die Oberfläche niemals einfriert.
- **1-Klick-Zwischenablage**:
  - Jeder Tab besitzt einen Button `In Zwischenablage kopieren` sowie einen `Speichern...`-Button.

---

## Befehlszeilen-Übersicht (CLI-Referenz)

```text
Aufruf: py-token-usage-reducer [-h] [--gui] [-v] <BEFEHL> ...

Globale Optionen:
  -h, --help            Hilfe anzeigen
  --gui                 Startet die PySide6 Desktop-Oberfläche
  -v, --verbose         Ausführliche Debug-Ausgaben aktivieren

Verfügbare Befehle:
  convert               Dokumente (PDF, DOCX, HTML, IPYNB) in Markdown wandeln
  report                Architektur- & Struktur-Report für Repositories erstellen
  skeleton              Python-Dateien auf Schnittstellen/Docstrings skelettieren
  schema                JSON-, CSV- und SQL-Dumps auf Schemas und Samples reduzieren
  compress-log          Logs und Tracebacks bereinigen und komprimieren
  trace-deps            Lokale Import-Abhängigkeiten gezielt bündeln
  diff-pack             Git-Diffs mit Schnittstellen-Kontext packen
  guide                 Umfassendes Handbuch & Anleitungen anzeigen
```

---

## Entwicklung & Qualitätssicherung

Das Projekt folgt strikten Qualitätsstandards:

```bash
# Test-Suite ausführen
uv run pytest

# Linter ausführen
uv run ruff check .

# Code-Formatierung prüfen & anwenden
uv run ruff format .
```

---

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
