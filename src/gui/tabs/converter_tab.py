"""GUI tab for Document to Markdown converter."""

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.gui.workers import TaskWorker
from src.modules.converter import convert_to_markdown


class ConverterTab(QWidget):
    """Tab widget for converting PDF, DOCX, HTML, and IPYNB files to clean Markdown."""

    def __init__(self) -> None:
        super().__init__()
        self.worker: TaskWorker | None = None
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # File selection section
        file_group = QGroupBox("Quelldatei auswählen")
        file_layout = QHBoxLayout(file_group)

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Wähle eine PDF-, DOCX-, HTML- oder IPYNB-Datei aus...")
        self.browse_btn = QPushButton("Durchsuchen...")
        self.browse_btn.setObjectName("secondaryButton")
        self.browse_btn.clicked.connect(self._browse_file)

        file_layout.addWidget(self.path_edit)
        file_layout.addWidget(self.browse_btn)
        layout.addWidget(file_group)

        # Options
        options_layout = QHBoxLayout()
        self.include_outputs_cb = QCheckBox("Code-Ausgaben bei Notebooks (.ipynb) beibehalten")
        self.convert_btn = QPushButton("In Markdown konvertieren")
        self.convert_btn.clicked.connect(self._start_conversion)

        options_layout.addWidget(self.include_outputs_cb)
        options_layout.addStretch()
        options_layout.addWidget(self.convert_btn)
        layout.addLayout(options_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Stats label
        self.stat_label = QLabel("Bereit zur Konvertierung.")
        self.stat_label.setObjectName("statLabel")
        layout.addWidget(self.stat_label)

        # Output editor
        self.output_edit = QPlainTextEdit()
        self.output_edit.setObjectName("codeView")
        self.output_edit.setPlaceholderText("Das bereinigte Markdown erscheint hier...")
        layout.addWidget(self.output_edit, stretch=1)

        # Bottom actions
        bottom_layout = QHBoxLayout()
        self.copy_btn = QPushButton("In Zwischenablage kopieren")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        self.save_btn = QPushButton("Als .md speichern...")
        self.save_btn.setObjectName("secondaryButton")
        self.save_btn.clicked.connect(self._save_file)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.copy_btn)
        bottom_layout.addWidget(self.save_btn)
        layout.addLayout(bottom_layout)

    def _browse_file(self) -> None:
        file_filter = "Unterstützte Dokumente (*.pdf *.docx *.html *.htm *.ipynb);;PDF (*.pdf);;Word (*.docx);;HTML (*.html *.htm);;Jupyter (*.ipynb);;Alle Dateien (*.*)"
        path, _ = QFileDialog.getOpenFileName(self, "Dokument auswählen", "", file_filter)
        if path:
            self.path_edit.setText(path)

    def _start_conversion(self) -> None:
        file_path = self.path_edit.text().strip()
        if not file_path or not Path(file_path).is_file():
            QMessageBox.warning(self, "Hinweis", "Bitte wähle eine gültige existierende Datei aus.")
            return

        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.stat_label.setText("Konvertierung läuft...")

        self.worker = TaskWorker(
            convert_to_markdown,
            file_path,
            include_outputs=self.include_outputs_cb.isChecked(),
        )
        self.worker.finished.connect(self._on_conversion_finished)
        self.worker.error.connect(self._on_conversion_error)
        self.worker.start()

    def _on_conversion_finished(self, result: Any) -> None:
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)

        markdown = result.get("markdown", "")
        self.output_edit.setPlainText(markdown)

        orig = result.get("estimated_raw_tokens", 0)
        reduced = result.get("reduced_tokens", 0)
        saved = result.get("tokens_saved", 0)
        pct = round((saved / orig * 100.0), 1) if orig > 0 else 0.0

        self.stat_label.setText(
            f"✓ Erfolgreich konvertiert! Tokens: {orig:,} → {reduced:,} "
            f"(Ersparnis: {saved:,} Tokens / -{pct}%)"
        )

    def _on_conversion_error(self, err_msg: str) -> None:
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        self.stat_label.setText("Fehler bei der Konvertierung.")
        QMessageBox.critical(self, "Fehler", f"Fehler bei der Konvertierung:\n{err_msg}")

    def _copy_to_clipboard(self) -> None:
        text = self.output_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.stat_label.setText("✓ Markdown in Zwischenablage kopiert!")

    def _save_file(self) -> None:
        text = self.output_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Markdown speichern", "output.md", "Markdown (*.md)"
        )
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self.stat_label.setText(f"✓ Gespeichert in: {Path(path).name}")
