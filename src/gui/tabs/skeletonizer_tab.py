"""GUI tab for Python AST Code Skeletonizer."""

from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
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
from src.modules.skeletonizer import skeletonize_code


class SkeletonizerTab(QWidget):
    """Tab widget for stripping function and method bodies from Python code."""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top bar with actions
        top_layout = QHBoxLayout()
        self.load_btn = QPushButton("Python-Datei laden...")
        self.load_btn.setObjectName("secondaryButton")
        self.load_btn.clicked.connect(self._load_file)

        self.keep_docstrings_cb = QCheckBox("Docstrings beibehalten")
        self.keep_docstrings_cb.setChecked(True)

        self.process_btn = QPushButton("Code skelettieren")
        self.process_btn.clicked.connect(self._process_code)

        top_layout.addWidget(self.load_btn)
        top_layout.addWidget(self.keep_docstrings_cb)
        top_layout.addStretch()
        top_layout.addWidget(self.process_btn)
        layout.addLayout(top_layout)

        # Stats label
        self.stat_label = QLabel("Code einfügen oder Datei laden.")
        self.stat_label.setObjectName("statLabel")
        layout.addWidget(self.stat_label)

        # Splitter with Source Code and Skeletonized Result
        splitter = QSplitter()

        # Left: Original code
        left_group = QGroupBox("Originaler Python-Quellcode")
        left_layout = QVBoxLayout(left_group)
        self.source_edit = QPlainTextEdit()
        self.source_edit.setObjectName("codeView")
        self.source_edit.setPlaceholderText("Füge hier Python-Quellcode ein...")
        left_layout.addWidget(self.source_edit)
        splitter.addWidget(left_group)

        # Right: Skeleton
        right_group = QGroupBox("Generiertes Schnittstellen-Skelett (ohne Rümpfe)")
        right_layout = QVBoxLayout(right_group)
        self.result_edit = QPlainTextEdit()
        self.result_edit.setObjectName("codeView")
        self.result_edit.setPlaceholderText("Das komprimierte Skelett erscheint hier...")
        right_layout.addWidget(self.result_edit)
        splitter.addWidget(right_group)

        splitter.setSizes([450, 450])
        layout.addWidget(splitter, stretch=1)

        # Bottom actions
        bottom_layout = QHBoxLayout()
        self.copy_btn = QPushButton("Skelett kopieren")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        self.save_btn = QPushButton("Als .py speichern...")
        self.save_btn.setObjectName("secondaryButton")
        self.save_btn.clicked.connect(self._save_file)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.copy_btn)
        bottom_layout.addWidget(self.save_btn)
        layout.addLayout(bottom_layout)

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Python-Datei laden", "", "Python (*.py);;Alle Dateien (*.*)"
        )
        if path:
            try:
                code = Path(path).read_text(encoding="utf-8", errors="ignore")
                self.source_edit.setPlainText(code)
                self.stat_label.setText(f"Datei geladen: {Path(path).name}")
            except OSError as exc:
                QMessageBox.critical(self, "Fehler", f"Datei konnte nicht gelesen werden:\n{exc}")

    def _process_code(self) -> None:
        raw_code = self.source_edit.toPlainText().strip()
        if not raw_code:
            QMessageBox.warning(self, "Hinweis", "Bitte gib zuerst Python-Quellcode ein.")
            return

        skeleton = skeletonize_code(raw_code, keep_docstrings=self.keep_docstrings_cb.isChecked())
        self.result_edit.setPlainText(skeleton)

        orig_tok = count_tokens(raw_code)
        skel_tok = count_tokens(skeleton)
        saved = max(0, orig_tok - skel_tok)
        pct = round((saved / orig_tok * 100.0), 1) if orig_tok > 0 else 0.0

        self.stat_label.setText(
            f"✓ Code skelettiert! Tokens: {orig_tok:,} → {skel_tok:,} "
            f"(Ersparnis: {saved:,} Tokens / -{pct}%)"
        )

    def _copy_to_clipboard(self) -> None:
        text = self.result_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.stat_label.setText("✓ Skelett in Zwischenablage kopiert!")

    def _save_file(self) -> None:
        text = self.result_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Skelett speichern", "skeleton.py", "Python (*.py)"
        )
        if path:
            Path(path).write_text(text, encoding="utf-8")
            self.stat_label.setText(f"✓ Gespeichert in: {Path(path).name}")
