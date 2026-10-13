"""Theme definitions and Qt Style Sheets (QSS) for Dark and Light modes."""

DARK_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
    color: #cdd6f4;
}

QTabWidget::pane {
    border: 1px solid #313244;
    background-color: #181825;
    border-radius: 6px;
    top: -1px;
}

QTabBar::tab {
    background-color: #1e1e2e;
    color: #a6adc8;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #313244;
    border-bottom: none;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #181825;
    color: #89b4fa;
    border-top: 2px solid #89b4fa;
}

QTabBar::tab:hover:!selected {
    background-color: #313244;
    color: #cdd6f4;
}

QPushButton {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    border-radius: 5px;
    padding: 7px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #b4befe;
}

QPushButton:pressed {
    background-color: #74c7ec;
}

QPushButton:disabled {
    background-color: #45475a;
    color: #6c7086;
}

QPushButton#secondaryButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
}

QPushButton#secondaryButton:hover {
    background-color: #45475a;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #11111b;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 5px;
    padding: 6px;
    selection-background-color: #89b4fa;
    selection-color: #11111b;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #89b4fa;
}

QPlainTextEdit#codeView {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    background-color: #0c0c14;
}

QScrollBar:vertical {
    border: none;
    background-color: #181825;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #45475a;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QCheckBox {
    spacing: 8px;
    color: #cdd6f4;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #45475a;
    background-color: #181825;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

QLabel#statLabel {
    color: #a6e3a1;
    font-weight: bold;
    padding: 4px;
}

QProgressBar {
    border: 1px solid #313244;
    border-radius: 5px;
    text-align: center;
    background-color: #11111b;
    color: #cdd6f4;
}

QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 4px;
}

QStatusBar {
    background-color: #11111b;
    color: #a6adc8;
    border-top: 1px solid #313244;
}
"""

LIGHT_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #eff1f5;
    color: #4c4f69;
}

QWidget {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
    color: #4c4f69;
}

QTabWidget::pane {
    border: 1px solid #ccd0da;
    background-color: #ffffff;
    border-radius: 6px;
    top: -1px;
}

QTabBar::tab {
    background-color: #e6e9ef;
    color: #6c6f85;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #ccd0da;
    border-bottom: none;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1e66f5;
    border-top: 2px solid #1e66f5;
}

QTabBar::tab:hover:!selected {
    background-color: #dce0e8;
    color: #4c4f69;
}

QPushButton {
    background-color: #1e66f5;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 7px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #04a5e5;
}

QPushButton:pressed {
    background-color: #209fb5;
}

QPushButton:disabled {
    background-color: #bcc0cc;
    color: #6c6f85;
}

QPushButton#secondaryButton {
    background-color: #e6e9ef;
    color: #4c4f69;
    border: 1px solid #ccd0da;
}

QPushButton#secondaryButton:hover {
    background-color: #dce0e8;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 5px;
    padding: 6px;
    selection-background-color: #1e66f5;
    selection-color: #ffffff;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #1e66f5;
}

QPlainTextEdit#codeView {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    background-color: #f4f5f8;
}

QScrollBar:vertical {
    border: none;
    background-color: #e6e9ef;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #acb0be;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #8c8fa1;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QCheckBox {
    spacing: 8px;
    color: #4c4f69;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid #acb0be;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #1e66f5;
    border-color: #1e66f5;
}

QLabel#statLabel {
    color: #40a02b;
    font-weight: bold;
    padding: 4px;
}

QProgressBar {
    border: 1px solid #ccd0da;
    border-radius: 5px;
    text-align: center;
    background-color: #ffffff;
    color: #4c4f69;
}

QProgressBar::chunk {
    background-color: #1e66f5;
    border-radius: 4px;
}

QStatusBar {
    background-color: #e6e9ef;
    color: #6c6f85;
    border-top: 1px solid #ccd0da;
}
"""
