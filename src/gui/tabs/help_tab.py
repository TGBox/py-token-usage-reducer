"""GUI tab providing comprehensive in-app user guide and documentation."""

from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.docs.manual import TOOL_DOCS, get_full_manual, get_tool_documentation


class HelpTab(QWidget):
    """Tab widget providing interactive documentation and usage instructions."""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header selection
        header_group = QGroupBox("Dokumentation & Anleitungen auswählen")
        header_layout = QHBoxLayout(header_group)

        label = QLabel("Thema:")
        self.tool_combo = QComboBox()
        self.tool_combo.addItem("📚 Gesamtübersicht & Handbuch", userData="")

        for cmd, doc in TOOL_DOCS.items():
            self.tool_combo.addItem(f"🛠️ {doc.name} ({cmd})", userData=cmd)

        self.tool_combo.currentIndexChanged.connect(self._on_selection_changed)

        header_layout.addWidget(label)
        header_layout.addWidget(self.tool_combo, stretch=1)
        layout.addWidget(header_group)

        # Content display
        self.doc_view = QPlainTextEdit()
        self.doc_view.setReadOnly(True)
        self.doc_view.setObjectName("codeView")
        layout.addWidget(self.doc_view, stretch=1)

        # Initial content
        self._on_selection_changed()

    def _on_selection_changed(self) -> None:
        cmd = self.tool_combo.currentData()
        if not cmd:
            text = get_full_manual()
        else:
            text = get_tool_documentation(cmd)
        self.doc_view.setPlainText(text)
