"""GUI tab for Log and Stacktrace Compressor."""

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
from src.modules.log_compressor import compress_logs


class LogCompressorTab(QWidget):
    """Tab widget for sanitizing terminal logs and collapsing deep framework tracebacks."""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top bar
        top_layout = QHBoxLayout()
        self.load_btn = QPushButton("Log-Datei laden...")
        self.load_btn.setObjectName("secondaryButton")
        self.load_btn.clicked.connect(self._load_file)

        self.compress_btn = QPushButton("Log komprimieren & bereinigen")
        self.compress_btn.clicked.connect(self._compress_log)

        top_layout.addWidget(self.load_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.compress_btn)
        layout.addLayout(top_layout)

        # Stats label
        self.stat_label = QLabel("Log-Text einfügen oder Datei laden.")
        self.stat_label.setObjectName("statLabel")
        layout.addWidget(self.stat_label)

        # Splitter with Raw Logs and Compressed Output
        splitter = QSplitter()

        # Left: Raw log
        left_group = QGroupBox("Unbereinigter Log-Output / Traceback")
        left_layout = QVBoxLayout(left_group)
        self.source_edit = QPlainTextEdit()
        self.source_edit.setObjectName("codeView")
        self.source_edit.setPlaceholderText(
            "Füge hier Terminal-Output, Stacktraces oder Server-Logs ein..."
        )
        left_layout.addWidget(self.source_edit)
        splitter.addWidget(left_group)

        # Right: Compressed log
        right_group = QGroupBox("Komprimierter, bereinigter Diagnose-Block")
        right_layout = QVBoxLayout(right_group)
        self.result_edit = QPlainTextEdit()
        self.result_edit.setObjectName("codeView")
        self.result_edit.setPlaceholderText("Der bereinigte Fehlerblock erscheint hier...")
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
        path, _ = QFileDialog.getOpenFileName(
            self, "Log-Datei laden", "", "Log-Dateien (*.log *.txt);;Alle Dateien (*.*)"
        )
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8", errors="ignore")
                self.source_edit.setPlainText(content)
                self.stat_label.setText(f"Datei geladen: {Path(path).name}")
            except OSError as exc:
                QMessageBox.critical(self, "Fehler", f"Datei konnte nicht gelesen werden:\n{exc}")

    def _compress_log(self) -> None:
        raw_text = self.source_edit.toPlainText().strip()
        if not raw_text:
            QMessageBox.warning(self, "Hinweis", "Bitte gib zuerst Log-Text ein.")
            return

        compressed = compress_logs(raw_text)
        self.result_edit.setPlainText(compressed)

        orig_tok = count_tokens(raw_text)
        comp_tok = count_tokens(compressed)
        saved = max(0, orig_tok - comp_tok)
        pct = round((saved / orig_tok * 100.0), 1) if orig_tok > 0 else 0.0

        self.stat_label.setText(
            f"✓ Log komprimiert! Tokens: {orig_tok:,} → {comp_tok:,} "
            f"(Ersparnis: {saved:,} Tokens / -{pct}%)"
        )

    def _copy_to_clipboard(self) -> None:
        text = self.result_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.stat_label.setText("✓ Bereinigter Log in Zwischenablage kopiert!")

    def _save_file(self) -> None:
        text = self.result_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Bereinigten Log speichern", "clean_log.md", "Markdown (*.md)"
        )
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self.stat_label.setText(f"✓ Gespeichert in: {Path(path).name}")
