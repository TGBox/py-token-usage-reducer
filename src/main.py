"""Main entry point for py-token-usage-reducer dispatching CLI commands or GUI."""

import sys

from src.cli.parser import run_cli


def main() -> None:
    # First check CLI arguments
    cli_args = sys.argv[1:]
    exit_code = run_cli(cli_args)

    # Exit code 100 indicates that GUI should be launched (e.g. no args or --gui)
    if exit_code == 100:
        # PySide6 + all tabs are heavy; CLI calls (e.g. from agent skills) shouldn't pay for them
        from PySide6.QtWidgets import QApplication

        from src.gui.app import MainWindow

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
