"""Comprehensive user manual and tool guide for CLI, GUI, and documentation export."""

from dataclasses import dataclass


@dataclass
class ToolDoc:
    command: str
    name: str
    summary: str
    when_to_use: str
    cli_usage: str
    gui_usage: str
    token_savings: str
    tips: str


TOOL_DOCS: dict[str, ToolDoc] = {
    "convert": ToolDoc(
        command="convert",
        name="Dokumenten-zu-Markdown-Konverter",
        summary="Konvertiert PDF-, Word- (DOCX), HTML- und Jupyter-Notebook-Dateien (.ipynb) in kompaktes, bereinigtes Markdown.",
        when_to_use=(
            "• Wenn du dem KI-Agenten externe Dokumentationen, Spezifikationen, Whitepaper oder Tutorials bereitstellen musst.\n"
            "• Wenn PDFs oder HTML-Seiten hunderte unleserliche Steuerzeichen, Script-Tags, Navigationsmenüs oder Base64-Bilder enthalten, "
            "die das Kontextfenster sofort überfüllen würden.\n"
            "• Wenn Jupyter Notebooks mit riesigen Diagrammen und Print-Ausgaben den Prompt sprengen."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer convert <DATEI> [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer convert spezifikation.pdf\n"
            "  py-token-usage-reducer convert handbuch.docx -o handbuch.md\n"
            "  py-token-usage-reducer convert doku.html --output clean_doku.md\n"
            "  py-token-usage-reducer convert analyse.ipynb --include-outputs\n\n"
            "Optionen:\n"
            "  -o, --output <DATEI>      Pfad zur Zieldatei (Standard: Ausgabe in Konsole)\n"
            "  --include-outputs         Gibt bei Notebooks auch Code-Ausgaben mit aus (Standard: deaktiviert zur Token-Ersparnis)"
        ),
        gui_usage=(
            "1. Öffne den Tab 'Konverter'.\n"
            "2. Wähle eine Datei (PDF, DOCX, HTML, IPYNB) über 'Datei auswählen' oder per Drag & Drop aus.\n"
            "3. Klicke auf 'In Markdown konvertieren'.\n"
            "4. Prüfe die Token-Ersparnis in den Statistiken und kopiere das Markdown mit 'In Zwischenablage kopieren' "
            "oder speichere es als .md-Datei."
        ),
        token_savings="Typisch 70 % bis 95 % im Vergleich zur Rohdatei bzw. Web-Dumps.",
        tips=(
            "Kopiere das generierte Markdown direkt in den Prompt deines Coding-Agenten. "
            "Die KI versteht Markdown-Strukturen (Überschriften, Listen, Code-Blöcke) schneller und fehlerfreier als rohe HTML- oder Binärinhalte."
        ),
    ),
    "report": ToolDoc(
        command="report",
        name="Projekt- & Architektur-Reporter",
        summary="Analysiert ein gesamtes Projektverzeichnis und generiert einen kompakten Architektur- und Struktur-Report.",
        when_to_use=(
            "• Zu Beginn einer neuen Session mit einem Coding-Agenten, um ihm den Gesamtzusammenhang des Projekts zu erklären.\n"
            "• Bei großen Codebasen (>10.000 Zeilen), bei denen es unmöglich oder viel zu teuer ist, alle Dateien komplett zu übergeben.\n"
            "• Um 'Top-Token-Verbraucher' zu identifizieren (welche Dateien im Repo fressen die meisten Tokens?)."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer report [PFAD] [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer report .\n"
            "  py-token-usage-reducer report /pfad/zum/projekt -o PROJECT_OVERVIEW.md\n"
            "  py-token-usage-reducer report . --skeletons --max-skeletons 8\n\n"
            "Optionen:\n"
            "  -o, --output <DATEI>      Speichert den Report als Markdown-Datei.\n"
            "  -s, --skeletons           Fügt Python-AST-Skelette der wichtigsten Module automatisch an den Report an.\n"
            "  --max-skeletons <N>       Maximale Anzahl an Dateien, deren Skelette eingebettet werden (Standard: 5)."
        ),
        gui_usage=(
            "1. Wechsle in den Tab 'Architektur-Report'.\n"
            "2. Wähle das gewünschte Projektverzeichnis aus.\n"
            "3. Aktiviere optional 'Code-Skelette einbetten'.\n"
            "4. Klicke auf 'Projekt analysieren'.\n"
            "5. Der fertige Report kann direkt in die Zwischenablage kopiert oder als PROJECT_SUMMARY.md gespeichert werden."
        ),
        token_savings="Spart 90 % bis 99 % im Vergleich zur Übergabe des gesamten Repositories.",
        tips=(
            "Der Report filtert automatisch .git, node_modules, .venv und alle Einträge deiner .gitignore-Datei heraus. "
            "Lege den Report als PROJECT_OVERVIEW.md im Repo ab, damit der Agent jederzeit darauf zugreifen kann."
        ),
    ),
    "skeleton": ToolDoc(
        command="skeleton",
        name="Python AST Code-Skelettierer",
        summary="Entfernt alle Funktions- und Methoden-Implementierungen und behält ausschließlich Signaturen, Typen und Docstrings.",
        when_to_use=(
            "• Wenn der Agent eine neue Funktion schreiben soll, die bestehende Schnittstellen aufruft, aber die Implementierungsdetails der anderen Module irrelevant sind.\n"
            "• Um APIs, Services oder Datenbank-Clients als Kontext zu übergeben, ohne Zehntausende Tokens für interne Berechnungen zu verschwenden.\n"
            "• Für saubere Architektur- und Modul-Übersichten."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer skeleton <DATEI> [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer skeleton src/services/database.py\n"
            "  py-token-usage-reducer skeleton src/main.py -o main_interface.py\n"
            "  py-token-usage-reducer skeleton src/api.py --no-docstrings\n\n"
            "Optionen:\n"
            "  -o, --output <DATEI>      Ausgabedatei festlegen.\n"
            "  --no-docstrings           Entfernt auch Docstrings (maximale Kompression)."
        ),
        gui_usage=(
            "1. Tab 'Code-Skelettierer' aufrufen.\n"
            "2. Python-Datei laden oder Quellcode direkt in das linke Textfeld einfügen.\n"
            "3. 'Code skelettieren' klicken.\n"
            "4. Im rechten Feld erscheint das saubere Schnittstellen-Skelett mit Anzeige der prozentualen Token-Ersparnis."
        ),
        token_savings="Regulär 60 % bis 85 % Ersparnis pro Python-Quelldatei.",
        tips=(
            "Da Docstrings und Typannotationen vollständig erhalten bleiben, weiß der Agent exakt, "
            "welche Parameter erwartet werden und wie die Schnittstelle funktioniert – ohne unnötigen Ballast."
        ),
    ),
    "schema": ToolDoc(
        command="schema",
        name="Data & Schema Reducer (JSON, CSV, SQL)",
        summary="Reduziert riesige Datenbestände auf Struktur, Schema und 2–3 exemplarische Beispieldatenzeilen.",
        when_to_use=(
            "• Wenn du dem Agenten eine Datenbanktabelle, ein CSV-Export oder eine API-Antwort zeigen musst, "
            "um eine Datenverarbeitung oder Abfrage zu implementieren.\n"
            "• Wenn ein JSON-Array 5.000 Einträge hat, der Agent aber nur wissen muss, welche Keys existieren.\n"
            "• Bei SQL-Dumps mit tausenden INSERT-Zeilen."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer schema <DATEI> [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer schema daten.json\n"
            "  py-token-usage-reducer schema kunden.csv --samples 3\n"
            "  py-token-usage-reducer schema backup.sql -o schema_only.sql\n\n"
            "Optionen:\n"
            "  -s, --samples <N>         Anzahl der beizubehaltenden Beispielzeilen (Standard: 3).\n"
            "  -o, --output <DATEI>      Ausgabepfad."
        ),
        gui_usage=(
            "1. Tab 'Schema-Reducer' öffnen.\n"
            "2. JSON, CSV oder SQL-Datei auswählen bzw. Text einfügen.\n"
            "3. 'Auf Schema reduzieren' wählen.\n"
            "4. Ergebnis prüfen und kopieren."
        ),
        token_savings="Häufig 90 % bis 99 % Token-Ersparnis bei großen Datensätzen.",
        tips=(
            "Der Agent benötigt für fast alle Programmieraufgaben (SQL-Queries, Pandas-Operationen, Pydantic-Modelle) "
            "ausschließlich Spaltennamen und Datentypen, keine zehntausend echten Datenzeilen."
        ),
    ),
    "compress-log": ToolDoc(
        command="compress-log",
        name="Log & Stacktrace Compressor",
        summary="Entfernt ANSI-Farbcodes, faltet sich wiederholende Zeilen zusammen und blendet interne Framework-Traceback-Frames aus.",
        when_to_use=(
            "• Beim Debugging von Fehlern, wenn das Terminal 300 Zeilen Log-Output oder gigantische Stacktraces ausgespuckt hat.\n"
            "• Wenn Frameworks (Django, FastAPI, PySide, React) endlose interne Zeilen aus site-packages/node_modules auflisten.\n"
            "• Wenn Logs von Polling-Requests oder Timern mit hunderten identischen Zeilen zugemüllt sind."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer compress-log <LOG_DATEI> [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer compress-log error.log\n"
            "  py-token-usage-reducer compress-log crash.txt -o clean_error.md"
        ),
        gui_usage=(
            "1. Tab 'Log-Kompressor' öffnen.\n"
            "2. Stacktrace oder Log-Text aus dem Terminal einfügen.\n"
            "3. 'Log komprimieren' drücken.\n"
            "4. Den bereinigten Fehlerblock mit einem Klick in den Prompt des Agenten kopieren."
        ),
        token_savings="Typisch 75 % bis 90 % Ersparnis bei Tracebacks und Terminal-Dumps.",
        tips=(
            "Der Kompressor isoliert die exakte Exception und den Anwendungs-Code, der den Fehler verursacht hat. "
            "Das verhindert, dass der Agent durch Bibliotheks-Code verwirrt wird."
        ),
    ),
    "trace-deps": ToolDoc(
        command="trace-deps",
        name="Smart Dependency Context Collector",
        summary="Analysiert die lokalen Imports einer Python-Einstiegsdatei und bündelt gezielt nur die tatsächlich benötigten Quellcodedateien.",
        when_to_use=(
            "• Wenn du an einem bestimmten Feature arbeitest und dem Agenten genau den relevanten Code-Kontext geben willst – "
            "weder zu wenig (fehlende Funktionen) noch zu viel (gesamtes Repo).\n"
            "• Um chirurgisch präzise Prompts für isolierte Refactorings zu bauen."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer trace-deps <EINSTIEGS_DATEI> [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer trace-deps src/main.py\n"
            "  py-token-usage-reducer trace-deps src/controllers/user.py --depth 2 -o user_context.md\n\n"
            "Optionen:\n"
            "  --depth <N>               Maximale Rekursionstiefe für lokale Imports (Standard: 3).\n"
            "  -o, --output <DATEI>      Ausgabedatei für das Kontext-Paket."
        ),
        gui_usage=(
            "1. Tab 'Import-Tracer' wählen.\n"
            "2. Einstiegsdatei auswählen.\n"
            "3. 'Abhängigkeiten bündeln' klicken.\n"
            "4. Das erzeugte Markdown enthält die Einstiegsdatei sowie alle rekursiv importierten Module in einem Block."
        ),
        token_savings="Spart 80 % bis 95 % gegenüber dem Kopieren ganzer Verzeichnisse.",
        tips=(
            "Externe Standardbibliotheken (wie os, sys, json) werden übersprungen – nur deine eigenen Projektdateien werden gesammelt."
        ),
    ),
    "diff-pack": ToolDoc(
        command="diff-pack",
        name="Git Diff Context Packager",
        summary="Kombiniert ungespeicherte Git-Änderungen mit den Schnittstellen-Skeletten der berührten Dateien.",
        when_to_use=(
            "• Wenn du den Coding-Agenten um ein Code-Review oder um das Schreiben von Tests für deine aktuellen Änderungen bittest.\n"
            "• Um einem Agenten zu zeigen, was sich geändert hat, ohne die kompletten unveränderten Dateien übertragen zu müssen.\n"
            "• Für automatische PR-Beschreibungen und Commit-Message-Generierung."
        ),
        cli_usage=(
            "Befehl: py-token-usage-reducer diff-pack [OPTIONEN]\n\n"
            "Beispiele:\n"
            "  py-token-usage-reducer diff-pack\n"
            "  py-token-usage-reducer diff-pack --staged\n"
            "  py-token-usage-reducer diff-pack -o current_changes.md\n\n"
            "Optionen:\n"
            "  --staged                  Verwendet staged Changes ('git diff --staged').\n"
            "  --no-skeletons            Hängt keine Schnittstellen-Skelette an, sondern nur den reinen Diff."
        ),
        gui_usage=(
            "1. Tab 'Git-Diff Packer' aufrufen.\n"
            "2. Bei Bedarf 'Staged Changes' aktivieren.\n"
            "3. 'Diff & Kontext laden' klicken.\n"
            "4. Das Paket enthält die geänderten Zeilen plus die Methodensignaturen der betroffenen Klassen."
        ),
        token_savings="Spart bis zu 90 % im Vergleich zur Übergabe vollständiger Dateien bei kleinen Diffs.",
        tips=(
            "Dadurch versteht der Agent auch bei einem 10-Zeilen-Diff den Kontext der umgebenden Klasse oder Datei, "
            "ohne dass du die gesamte Datei übertragen musst."
        ),
    ),
}


def get_tool_documentation(command: str | None = None) -> str:
    """Retrieve detailed documentation for a single tool or a quick index."""
    if not command:
        return get_full_manual()

    doc = TOOL_DOCS.get(command.lower().strip())
    if not doc:
        valid_commands = ", ".join(TOOL_DOCS.keys())
        return (
            f"Unbekanntes Werkzeug '{command}'.\n"
            f"Verfügbare Werkzeuge: {valid_commands}\n"
            f"Verwende 'py-token-usage-reducer guide' für die Gesamtübersicht."
        )

    lines: list[str] = [
        f"# {doc.name} (`{doc.command}`)",
        f"{doc.summary}",
        "",
        "## 💡 Wann ist diese Funktion nützlich?",
        doc.when_to_use,
        "",
        "## 💻 Ausführung über die Befehlszeile (CLI)",
        f"```text\n{doc.cli_usage}\n```",
        "",
        "## 🖥️ Ausführung über die Desktop-GUI",
        doc.gui_usage,
        "",
        "## 📉 Typische Token-Ersparnis",
        f"**{doc.token_savings}**",
        "",
        "## 🎯 Praxistipps & Best Practices",
        doc.tips,
    ]
    return "\n".join(lines)


def get_full_manual() -> str:
    """Generate the full comprehensive user manual across all integrated tools."""
    sections: list[str] = [
        "# py-token-usage-reducer – Ausführliches Benutzerhandbuch",
        "",
        (
            "Willkommen bei **py-token-usage-reducer**, deiner lokalen Schaltzentrale zur drastischen "
            "Reduzierung von Token-Kosten und Kontext-Fenster-Überläufen bei der Arbeit mit KI-Coding-Agenten."
        ),
        "",
        "## Übersicht der verfügbaren Werkzeuge",
        "| Befehl | Werkzeug | Hauptzweck | Typische Ersparnis |",
        "|---|---|---|---|",
    ]

    for tool in TOOL_DOCS.values():
        sections.append(
            f"| `{tool.command}` | {tool.name} | {tool.summary[:60]}... | {tool.token_savings[:20]} |"
        )

    sections.extend(["", "---", ""])

    for tool in TOOL_DOCS.values():
        sections.append(get_tool_documentation(tool.command))
        sections.extend(["", "---", ""])

    sections.extend(
        [
            "## Tastaturkürzel in der Desktop-GUI",
            "- **F11**: Umschalten zwischen Vollbildmodus und Fensteransicht.",
            "- **Strg+Q** (oder Alt+F4): Anwendung beenden.",
            "- **Theme-Umschalter**: Wechsel zwischen Dark Mode und Light Mode in der Menüleiste.",
            "",
            "## Allgemeine Best Practices zur Token-Reduzierung",
            "1. **Vorfiltern statt blindem Kopieren**: Übergib niemals vollständige Bibliotheken oder Dumps an den Agenten.",
            "2. **Skelette für Schnittstellen**: Wenn der Agent Code nutzt, den er nicht bearbeiten soll, reicht das AST-Skelett.",
            "3. **Repräsentative Stichproben für Daten**: Bei JSON und CSV reichen Spalten und 2-3 Zeilen völlig aus.",
            "4. **Lokale Ausführung**: Alle Reduktionen in diesem Programm laufen 100 % lokal ohne Internetverbindung und ohne API-Kosten.",
        ]
    )

    return "\n".join(sections)
