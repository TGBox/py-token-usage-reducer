"""Tests for PySide6 Desktop GUI."""

import os
import sys

from PySide6.QtWidgets import QApplication

from src.gui.app import MainWindow


def test_main_window_tabs():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    _ = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()

    assert window.tabs.count() == 8
    assert "Konverter" in window.tabs.tabText(0)
    assert "Architektur-Report" in window.tabs.tabText(1)
    assert "Code-Skelette" in window.tabs.tabText(2)
    assert "Schema-Reducer" in window.tabs.tabText(3)
    assert "Log-Kompressor" in window.tabs.tabText(4)
    assert "Kontext-Packer" in window.tabs.tabText(5)
    assert "Token-Budget" in window.tabs.tabText(6)
    assert "Hilfe & Handbuch" in window.tabs.tabText(7)

    window.show()

    # Test fullscreen toggle
    window.toggle_fullscreen()
    assert window.isFullScreen()
    window.toggle_fullscreen()
    assert not window.isFullScreen()

    # Test theme toggling
    window.set_theme("light")
    assert window.current_theme == "light"
    window.set_theme("dark")
    assert window.current_theme == "dark"
