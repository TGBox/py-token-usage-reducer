"""GUI tab for Data and Schema Reducer (JSON, CSV, SQL)."""

from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.core.tokenizer import count_tokens
from src.modules.data_reducer import reduce_csv, reduce_json, reduce_sql


class DataReducerTab(QWidget):
    """Tab widget for reducing large JSON, CSV, and SQL dumps into schemas and sample rows."""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top bar with controls
        top_layout = QHBoxLayout()
        self.load_btn = QPushButton("Datei laden (JSON, CSV, SQL)...")
        self.load_btn.setObjectName("secondaryButton")
        self.load_btn.clicked.connect(self._load_file)

        self.reduce_btn = QPushButton("Auf Schema & Samples reduzieren")
        self.reduce_btn.clicked.connect(self._process_data)

        top_layout.addWidget(self.load_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.reduce_btn)
        layout.addLayout(top_layout)

        # Stats label
        self.stat_label = QLabel("Daten einfügen oder Datei laden.")
        self.stat_label.setObjectName("statLabel")
        layout.addWidget(self.stat_label)

        # Splitter with Source and Reduced Result
        splitter = QSplitter()

        # Left: Original data
        left_group = QGroupBox("Quelldaten (JSON, CSV oder SQL)")
        left_layout = QVBoxLayout(left_group)
        self.source_edit = QPlainTextEdit()
        self.source_edit.setObjectName("codeView")
        self.source_edit.setPlaceholderText("Füge hier JSON, CSV-Daten oder einen SQL-Dump ein...")
        left_layout.addWidget(self.source_edit)
        splitter.addWidget(left_group)

        # Right: Reduced schema
        right_group = QGroupBox("Reduziertes Schema mit Stichproben")
        right_layout = QVBoxLayout(right_group)
        self.result_edit = QPlainTextEdit()
        self.result_edit.setObjectName("codeView")
        self.result_edit.setPlaceholderText("Das bereinigte Schema erscheint hier...")
        right_layout.addWidget(self.result_edit)
        splitter.addWidget(right_group)

        splitter.setSizes([450, 450])
        layout.addWidget(splitter, stretch=1)

        # Bottom actions
        bottom_layout = QHBoxLayout()
        self.copy_btn = QPushButton("In Zwischenablage kopieren")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        self.save_btn = QPushButton("Speichern...")
        self.save_btn.setObjectName("secondaryButton")
        self.save_btn.clicked.connect(self._save_file)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.copy_btn)
        bottom_layout.addWidget(self.save_btn)
        layout.addLayout(bottom_layout)

    def _load_file(self) -> None:
        filter_str = "Datendateien (*.json *.csv *.sql *.tsv);;JSON (*.json);;CSV (*.csv);;SQL (*.sql);;Alle Dateien (*.*)"
        path, _ = QFileDialog.getOpenFileName(self, "Datendatei laden", "", filter_str)
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8", errors="ignore")
                self.source_edit.setPlainText(content)
                self.stat_label.setText(f"Datei geladen: {Path(path).name}")
            except OSError as exc:
                QMessageBox.critical(self, "Fehler", f"Datei konnte nicht gelesen werden:\n{exc}")

    def _process_data(self) -> None:
        raw_text = self.source_edit.toPlainText().strip()
        if not raw_text:
            QMessageBox.warning(self, "Hinweis", "Bitte gib zuerst Daten ein.")
            return

        # Auto-detect format
        reduced = ""
        if raw_text.startswith(("{", "[")):
            try:
                reduced = reduce_json(raw_text, max_samples=3)
            except (ValueError, TypeError):
                reduced = ""

        if not reduced and (
            "CREATE TABLE" in raw_text.upper() or "INSERT INTO" in raw_text.upper()
        ):
            reduced = reduce_sql(raw_text, max_inserts=2)

        if not reduced:
            # Fallback to CSV
            try:
                reduced = reduce_csv(raw_text, max_rows=3)
            except (ValueError, TypeError):
                reduced = raw_text

        self.result_edit.setPlainText(reduced)

        orig_tok = count_tokens(raw_text)
        red_tok = count_tokens(reduced)
        saved = max(0, orig_tok - red_tok)
        pct = round((saved / orig_tok * 100.0), 1) if orig_tok > 0 else 0.0

        self.stat_label.setText(
            f"✓ Schema extrahiert! Tokens: {orig_tok:,} → {red_tok:,} "
            f"(Ersparnis: {saved:,} Tokens / -{pct}%)"
        )

    def _copy_to_clipboard(self) -> None:
        text = self.result_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.stat_label.setText("✓ Schema in Zwischenablage kopiert!")

    def _save_file(self) -> None:
        text = self.result_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Schema speichern", "schema.md", "Markdown (*.md)"
        )
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self.stat_label.setText(f"✓ Gespeichert in: {Path(path).name}")
