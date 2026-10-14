"""GUI tab for live token counting and context budget inspection."""

from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.tokenizer import count_tokens, estimate_token_cost


class TokenInspectorTab(QWidget):
    """Tab widget for measuring token consumption and inspecting context limits."""

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top Bar
        top_layout = QHBoxLayout()
        self.load_btn = QPushButton("Beliebige Datei laden...")
        self.load_btn.setObjectName("secondaryButton")
        self.load_btn.clicked.connect(self._load_file)

        self.clear_btn = QPushButton("Text leeren")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.clicked.connect(self._clear_text)

        top_layout.addWidget(self.load_btn)
        top_layout.addWidget(self.clear_btn)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        # Text input
        self.text_edit = QPlainTextEdit()
        self.text_edit.setObjectName("codeView")
        self.text_edit.setPlaceholderText(
            "Füge hier beliebigen Text, Code oder Prompt-Inhalte ein, um die Token-Nutzung live zu berechnen..."
        )
        # Recount only after typing pauses; tiktoken over a large paste on every keystroke lags
        self._recount_timer = QTimer(self)
        self._recount_timer.setSingleShot(True)
        self._recount_timer.setInterval(300)
        self._recount_timer.timeout.connect(self._update_metrics)
        self.text_edit.textChanged.connect(self._recount_timer.start)
        layout.addWidget(self.text_edit, stretch=1)

        # Metrics Card
        metrics_group = QGroupBox("Token- & Kontext-Budget Metriken")
        metrics_layout = QVBoxLayout(metrics_group)

        self.summary_label = QLabel("0 Tokens | 0 Zeichen | 0 Zeilen")
        self.summary_label.setObjectName("statLabel")
        metrics_layout.addWidget(self.summary_label)

        # Context limit progress bars
        # 1. 32k limit
        layout_32k = QHBoxLayout()
        self.label_32k = QLabel("32k Kontextfenster (Standard/Lokale Modelle):")
        self.bar_32k = QProgressBar()
        self.bar_32k.setRange(0, 32_000)
        self.bar_32k.setValue(0)
        layout_32k.addWidget(self.label_32k)
        layout_32k.addWidget(self.bar_32k)
        metrics_layout.addLayout(layout_32k)

        # 2. 128k limit
        layout_128k = QHBoxLayout()
        self.label_128k = QLabel("128k Kontextfenster (GPT-4o / gängige Modelle):")
        self.bar_128k = QProgressBar()
        self.bar_128k.setRange(0, 128_000)
        self.bar_128k.setValue(0)
        layout_128k.addWidget(self.label_128k)
        layout_128k.addWidget(self.bar_128k)
        metrics_layout.addLayout(layout_128k)

        # 3. 200k limit
        layout_200k = QHBoxLayout()
        self.label_200k = QLabel("200k Kontextfenster (Claude 3.5 Sonnet):")
        self.bar_200k = QProgressBar()
        self.bar_200k.setRange(0, 200_000)
        self.bar_200k.setValue(0)
        layout_200k.addWidget(self.label_200k)
        layout_200k.addWidget(self.bar_200k)
        metrics_layout.addLayout(layout_200k)

        # Cost Estimate Label
        self.cost_label = QLabel("Geschätzte Kosten pro Durchlauf: ~0.00 $")
        metrics_layout.addWidget(self.cost_label)

        layout.addWidget(metrics_group)

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Datei für Token-Zählung laden", "", "Alle Dateien (*.*)"
        )
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8", errors="ignore")
                self.text_edit.setPlainText(content)
            except OSError as exc:
                QMessageBox.critical(self, "Fehler", f"Datei konnte nicht geladen werden:\n{exc}")

    def _clear_text(self) -> None:
        self.text_edit.clear()

    def _update_metrics(self) -> None:
        text = self.text_edit.toPlainText()
        char_count = len(text)
        line_count = len(text.splitlines()) if text else 0
        tok_count = count_tokens(text)

        self.summary_label.setText(
            f"📊 **{tok_count:,} Tokens** | {char_count:,} Zeichen | {line_count:,} Zeilen"
        )

        self.bar_32k.setValue(min(32_000, tok_count))
        self.bar_128k.setValue(min(128_000, tok_count))
        self.bar_200k.setValue(min(200_000, tok_count))

        # Costs
        cost_sonnet = estimate_token_cost(tok_count, "claude-3-5-sonnet")
        cost_gpt4o = estimate_token_cost(tok_count, "gpt-4o")
        cost_mini = estimate_token_cost(tok_count, "gpt-4o-mini")

        self.cost_label.setText(
            f"Geschätzte Input-Kosten pro Anfrage: "
            f"Claude 3.5 Sonnet: ${cost_sonnet:.5f} | "
            f"GPT-4o: ${cost_gpt4o:.5f} | "
            f"GPT-4o-mini: ${cost_mini:.5f}"
        )
