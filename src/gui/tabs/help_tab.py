"""GUI tab providing rendered Markdown documentation and usage instructions."""

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from src.docs.manual import TOOL_DOCS, get_full_manual, get_tool_documentation


class HelpTab(QWidget):
    """Tab widget providing rich-text rendered documentation and usage instructions."""

    def __init__(self) -> None:
        super().__init__()
        self._current_raw_text = ""
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header selection & controls
        header_group = QGroupBox("Dokumentation & Anleitungen")
        header_layout = QHBoxLayout(header_group)

        label = QLabel("Thema:")
        self.tool_combo = QComboBox()
        self.tool_combo.addItem("📚 Gesamtübersicht & Handbuch", userData="")

        for cmd, doc in TOOL_DOCS.items():
            self.tool_combo.addItem(f"🛠️ {doc.name} ({cmd})", userData=cmd)

        self.tool_combo.currentIndexChanged.connect(self._on_selection_changed)

        self.raw_view_cb = QCheckBox("Roh-Markdown anzeigen")
        self.raw_view_cb.toggled.connect(self._render_current_text)

        self.copy_btn = QPushButton("In Zwischenablage kopieren")
        self.copy_btn.setObjectName("secondaryButton")
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        header_layout.addWidget(label)
        header_layout.addWidget(self.tool_combo, stretch=1)
        header_layout.addWidget(self.raw_view_cb)
        header_layout.addWidget(self.copy_btn)
        layout.addWidget(header_group)

        # Rich text browser rendering Markdown
        self.doc_view = QTextBrowser()
        self.doc_view.setObjectName("helpBrowser")
        self.doc_view.setOpenExternalLinks(True)
        layout.addWidget(self.doc_view, stretch=1)

        # Initial content
        self._on_selection_changed()

    def _on_selection_changed(self) -> None:
        cmd = self.tool_combo.currentData()
        if not cmd:
            self._current_raw_text = get_full_manual()
        else:
            self._current_raw_text = get_tool_documentation(cmd)
        self._render_current_text()

    def _render_current_text(self) -> None:
        if self.raw_view_cb.isChecked():
            self.doc_view.setPlainText(self._current_raw_text)
        else:
            self.doc_view.setMarkdown(self._current_raw_text)

    def _copy_to_clipboard(self) -> None:
        if self._current_raw_text:
            QApplication.clipboard().setText(self._current_raw_text)
