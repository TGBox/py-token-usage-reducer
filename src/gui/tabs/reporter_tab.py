"""GUI tab for Project Architecture & Codebase Reporter."""

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
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.gui.workers import TaskWorker
from src.modules.reporter import generate_project_report


class ReporterTab(QWidget):
    """Tab widget for analyzing project directories and generating architectural reports."""

    def __init__(self) -> None:
        super().__init__()
        self.worker: TaskWorker | None = None
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Directory selection
        dir_group = QGroupBox("Projektverzeichnis auswählen")
        dir_layout = QHBoxLayout(dir_group)

        self.path_edit = QLineEdit(str(Path.cwd()))
        self.browse_btn = QPushButton("Ordner wählen...")
        self.browse_btn.setObjectName("secondaryButton")
        self.browse_btn.clicked.connect(self._browse_dir)

        dir_layout.addWidget(self.path_edit)
        dir_layout.addWidget(self.browse_btn)
        layout.addWidget(dir_group)

        # Options
        options_layout = QHBoxLayout()
        self.skeletons_cb = QCheckBox("Code-Skelette wichtiger Module einbetten")
        self.skeletons_cb.setChecked(True)

        self.max_skel_spin = QSpinBox()
        self.max_skel_spin.setRange(1, 30)
        self.max_skel_spin.setValue(5)
        self.max_skel_spin.setPrefix("Max. ")
        self.max_skel_spin.setSuffix(" Dateien")

        self.analyze_btn = QPushButton("Projekt analysieren")
        self.analyze_btn.clicked.connect(self._start_analysis)

        options_layout.addWidget(self.skeletons_cb)
        options_layout.addWidget(self.max_skel_spin)
        options_layout.addStretch()
        options_layout.addWidget(self.analyze_btn)
        layout.addLayout(options_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Stats label
        self.stat_label = QLabel("Bereit zur Codebase-Analyse.")
        self.stat_label.setObjectName("statLabel")
        layout.addWidget(self.stat_label)

        # Output editor
        self.output_edit = QPlainTextEdit()
        self.output_edit.setObjectName("codeView")
        self.output_edit.setPlaceholderText("Der generierte Architektur-Report erscheint hier...")
        layout.addWidget(self.output_edit, stretch=1)

        # Bottom actions
        bottom_layout = QHBoxLayout()
        self.copy_btn = QPushButton("In Zwischenablage kopieren")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        self.save_btn = QPushButton("Als PROJECT_OVERVIEW.md speichern...")
        self.save_btn.setObjectName("secondaryButton")
        self.save_btn.clicked.connect(self._save_file)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.copy_btn)
        bottom_layout.addWidget(self.save_btn)
        layout.addLayout(bottom_layout)

    def _browse_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self, "Projektordner auswählen", self.path_edit.text()
        )
        if path:
            self.path_edit.setText(path)

    def _start_analysis(self) -> None:
        dir_path = self.path_edit.text().strip()
        if not dir_path or not Path(dir_path).is_dir():
            QMessageBox.warning(self, "Hinweis", "Bitte wähle ein gültiges Verzeichnis aus.")
            return

        self.analyze_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.stat_label.setText("Analysiere Projekt und extrahiere Architekturdaten...")

        self.worker = TaskWorker(
            generate_project_report,
            dir_path,
            include_skeletons=self.skeletons_cb.isChecked(),
            max_skeleton_files=self.max_skel_spin.value(),
        )
        self.worker.result.connect(self._on_analysis_finished)
        self.worker.error.connect(self._on_analysis_error)
        self.worker.start()

    def _on_analysis_finished(self, result: Any) -> None:
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)

        md = result.get("markdown", "")
        self.output_edit.setPlainText(md)

        files = result.get("total_files", 0)
        tokens = result.get("total_tokens", 0)
        cost = result.get("estimated_cost_usd", 0.0)

        self.stat_label.setText(
            f"✓ Analyse abgeschlossen! {files} Dateien geprüft, {tokens:,} Tokens Gesamtprojekt "
            f"(~${cost:.4f} geschätzt für Claude Sonnet 5.5)."
        )

    def _on_analysis_error(self, err_msg: str) -> None:
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.stat_label.setText("Fehler bei der Analyse.")
        QMessageBox.critical(self, "Fehler", f"Fehler bei der Analyse:\n{err_msg}")

    def _copy_to_clipboard(self) -> None:
        text = self.output_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.stat_label.setText("✓ Report in Zwischenablage kopiert!")

    def _save_file(self) -> None:
        text = self.output_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Report speichern", "PROJECT_OVERVIEW.md", "Markdown (*.md)"
        )
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self.stat_label.setText(f"✓ Gespeichert in: {Path(path).name}")
