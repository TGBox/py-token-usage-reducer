"""GUI tab combining Smart Dependency Context Collector and Git Diff Packager."""

from pathlib import Path

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
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.modules.dep_tracer import trace_dependencies
from src.modules.diff_packager import package_git_diff


class ContextPackagerTab(QWidget):
    """Tab widget for bundling targeted code context via import-tracing or git diffs."""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Mode Selector
        mode_group = QGroupBox("Paketierungs-Modus")
        mode_layout = QHBoxLayout(mode_group)
        self.mode_deps_rb = QRadioButton("Import-Tracer (Ausgehend von Einstiegsdatei)")
        self.mode_deps_rb.setChecked(True)
        self.mode_deps_rb.toggled.connect(self._toggle_mode)

        self.mode_diff_rb = QRadioButton("Git-Diff Packer (Geänderte Dateien + Schnittstellen)")
        self.mode_diff_rb.toggled.connect(self._toggle_mode)

        mode_layout.addWidget(self.mode_deps_rb)
        mode_layout.addWidget(self.mode_diff_rb)
        mode_layout.addStretch()
        layout.addWidget(mode_group)

        # Settings for Import Tracer
        self.deps_group = QGroupBox("Import-Tracer Einstellungen")
        deps_layout = QHBoxLayout(self.deps_group)

        self.entry_edit = QLineEdit()
        self.entry_edit.setPlaceholderText(
            "Wähle eine Python-Einstiegsdatei (z. B. src/main.py)..."
        )
        self.entry_browse_btn = QPushButton("Durchsuchen...")
        self.entry_browse_btn.setObjectName("secondaryButton")
        self.entry_browse_btn.clicked.connect(self._browse_entry_file)

        self.depth_spin = QSpinBox()
        self.depth_spin.setRange(1, 10)
        self.depth_spin.setValue(3)
        self.depth_spin.setPrefix("Tiefe: ")

        deps_layout.addWidget(self.entry_edit)
        deps_layout.addWidget(self.entry_browse_btn)
        deps_layout.addWidget(self.depth_spin)
        layout.addWidget(self.deps_group)

        # Settings for Git Diff
        self.diff_group = QGroupBox("Git-Diff Einstellungen")
        diff_layout = QHBoxLayout(self.diff_group)

        self.staged_cb = QCheckBox("Nur Staged Changes (--staged)")
        self.diff_skel_cb = QCheckBox("Schnittstellen-Skelette der betroffenen Dateien einbetten")
        self.diff_skel_cb.setChecked(True)

        diff_layout.addWidget(self.staged_cb)
        diff_layout.addWidget(self.diff_skel_cb)
        diff_layout.addStretch()
        layout.addWidget(self.diff_group)
        self.diff_group.setVisible(False)

        # Action button & status
        action_layout = QHBoxLayout()
        self.stat_label = QLabel("Bereit zum Packen.")
        self.stat_label.setObjectName("statLabel")

        self.package_btn = QPushButton("Kontext-Paket generieren")
        self.package_btn.clicked.connect(self._generate_package)

        action_layout.addWidget(self.stat_label)
        action_layout.addStretch()
        action_layout.addWidget(self.package_btn)
        layout.addLayout(action_layout)

        # Output editor
        self.output_edit = QPlainTextEdit()
        self.output_edit.setObjectName("codeView")
        self.output_edit.setPlaceholderText(
            "Das gebündelte Markdown-Kontextpaket erscheint hier..."
        )
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

    def _toggle_mode(self) -> None:
        is_deps = self.mode_deps_rb.isChecked()
        self.deps_group.setVisible(is_deps)
        self.diff_group.setVisible(not is_deps)

    def _browse_entry_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Einstiegsdatei wählen", "", "Python (*.py);;Alle Dateien (*.*)"
        )
        if path:
            self.entry_edit.setText(path)

    def _generate_package(self) -> None:
        if self.mode_deps_rb.isChecked():
            entry_path = self.entry_edit.text().strip()
            if not entry_path or not Path(entry_path).is_file():
                QMessageBox.warning(
                    self, "Hinweis", "Bitte wähle eine gültige existierende Einstiegsdatei aus."
                )
                return

            res = trace_dependencies(entry_path, max_depth=self.depth_spin.value())
            md = res.get("bundled_markdown", "")
            files_count = len(res.get("dependency_files", []))
            tokens = res.get("tokens", 0)

            self.output_edit.setPlainText(md)
            self.stat_label.setText(f"✓ {files_count} Datei(en) gebündelt ({tokens:,} Tokens).")

        else:
            res = package_git_diff(
                Path.cwd(),
                staged=self.staged_cb.isChecked(),
                include_skeletons=self.diff_skel_cb.isChecked(),
            )
            md = res.get("packaged_markdown", "")
            files_count = len(res.get("diff_files", []))
            tokens = res.get("tokens", 0)

            self.output_edit.setPlainText(md)
            self.stat_label.setText(
                f"✓ Git-Diff geladen: {files_count} geänderte Datei(en) ({tokens:,} Tokens)."
            )

    def _copy_to_clipboard(self) -> None:
        text = self.output_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.stat_label.setText("✓ Paket in Zwischenablage kopiert!")

    def _save_file(self) -> None:
        text = self.output_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Paket speichern", "context_bundle.md", "Markdown (*.md)"
        )
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self.stat_label.setText(f"✓ Gespeichert in: {Path(path).name}")
