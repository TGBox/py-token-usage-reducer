"""Main PySide6 application window with tabs, F11 fullscreen toggle, and QSettings persistence."""

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from src.gui.tabs.context_packager_tab import ContextPackagerTab
from src.gui.tabs.converter_tab import ConverterTab
from src.gui.tabs.data_reducer_tab import DataReducerTab
from src.gui.tabs.help_tab import HelpTab
from src.gui.tabs.log_compressor_tab import LogCompressorTab
from src.gui.tabs.reporter_tab import ReporterTab
from src.gui.tabs.skeletonizer_tab import SkeletonizerTab
from src.gui.tabs.token_inspector_tab import TokenInspectorTab
from src.gui.theme import DARK_THEME_QSS, LIGHT_THEME_QSS


class MainWindow(QMainWindow):
    """Main desktop application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("py-token-usage-reducer – Token-Optimierer für Coding-Agenten")
        self.settings = QSettings("DaniBani", "PyTokenUsageReducer")
        self.current_theme = "dark"

        self._setup_ui()
        self._setup_menu()
        self._load_settings()

    def _setup_ui(self) -> None:
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Initialize individual tool tabs
        self.converter_tab = ConverterTab()
        self.reporter_tab = ReporterTab()
        self.skeletonizer_tab = SkeletonizerTab()
        self.data_reducer_tab = DataReducerTab()
        self.log_compressor_tab = LogCompressorTab()
        self.packager_tab = ContextPackagerTab()
        self.inspector_tab = TokenInspectorTab()
        self.help_tab = HelpTab()

        self.tabs.addTab(self.converter_tab, "📄 Konverter")
        self.tabs.addTab(self.reporter_tab, "🏗️ Architektur-Report")
        self.tabs.addTab(self.skeletonizer_tab, "🦴 Code-Skelette")
        self.tabs.addTab(self.data_reducer_tab, "📊 Schema-Reducer")
        self.tabs.addTab(self.log_compressor_tab, "📋 Log-Kompressor")
        self.tabs.addTab(self.packager_tab, "📦 Kontext-Packer")
        self.tabs.addTab(self.inspector_tab, "🔢 Token-Budget")
        self.tabs.addTab(self.help_tab, "❓ Hilfe & Handbuch")

        self.setCentralWidget(self.tabs)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Bereit. Drücke F11 für Vollbildmodus.")

    def _setup_menu(self) -> None:
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("Datei")
        exit_action = QAction("Beenden", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menu_bar.addMenu("Ansicht")

        # F11 Fullscreen Action
        self.fullscreen_action = QAction("Vollbildmodus umschalten (F11)", self)
        self.fullscreen_action.setShortcut(QKeySequence(Qt.Key.Key_F11))
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(self.fullscreen_action)

        view_menu.addSeparator()

        # Theme toggles
        self.dark_action = QAction("Dunkles Design (Dark Mode)", self)
        self.dark_action.setCheckable(True)
        self.dark_action.setChecked(True)
        self.dark_action.triggered.connect(lambda: self.set_theme("dark"))
        view_menu.addAction(self.dark_action)

        self.light_action = QAction("Helles Design (Light Mode)", self)
        self.light_action.setCheckable(True)
        self.light_action.setChecked(False)
        self.light_action.triggered.connect(lambda: self.set_theme("light"))
        view_menu.addAction(self.light_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Hilfe")
        open_guide_action = QAction("Handbuch anzeigen", self)
        open_guide_action.triggered.connect(self._open_help_tab)
        help_menu.addAction(open_guide_action)

        about_action = QAction("Über py-token-usage-reducer", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def toggle_fullscreen(self) -> None:
        """Toggle seamlessly between windowed and fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
            self.statusBar().showMessage("Fenstermodus aktiv (F11 für Vollbild).", 3000)
        else:
            self.showFullScreen()
            self.statusBar().showMessage("Vollbildmodus aktiv (F11 zum Beenden).", 3000)

    def set_theme(self, theme_name: str) -> None:
        """Apply selected stylesheet theme."""
        self.current_theme = theme_name
        if theme_name == "light":
            QApplication.instance().setStyleSheet(LIGHT_THEME_QSS)
            self.dark_action.setChecked(False)
            self.light_action.setChecked(True)
        else:
            QApplication.instance().setStyleSheet(DARK_THEME_QSS)
            self.dark_action.setChecked(True)
            self.light_action.setChecked(False)

    def _open_help_tab(self) -> None:
        self.tabs.setCurrentWidget(self.help_tab)

    def _show_about(self) -> None:
        QMessageBox.information(
            self,
            "Über py-token-usage-reducer",
            "py-token-usage-reducer v0.1.0\n\n"
            "Eine modulare, 100 % lokale Desktop- und CLI-Anwendung zur Reduzierung "
            "von Token-Kosten und Kontextfenster-Überläufen bei der Arbeit mit Coding-Agenten.\n\n"
            "Entwickelt für Entwickler mit Datenschutz im Fokus.",
        )

    def _load_settings(self) -> None:
        """Restore window geometry, state, and theme from QSettings."""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(1100, 750)

        theme = self.settings.value("theme", "dark")
        self.set_theme(str(theme))

        tab_idx = self.settings.value("active_tab", 0)
        try:
            self.tabs.setCurrentIndex(int(tab_idx))
        except (ValueError, TypeError):
            pass

        if self.settings.value("is_fullscreen", False, type=bool):
            self.showFullScreen()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Persist settings upon exit."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("theme", self.current_theme)
        self.settings.setValue("active_tab", self.tabs.currentIndex())
        self.settings.setValue("is_fullscreen", self.isFullScreen())
        super().closeEvent(event)
