"""Asynchronous task execution using QThread and Qt Signals to prevent GUI freezing."""

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QThread, Signal


class TaskWorker(QThread):
    """Generic worker thread executing heavy reducer/scanner functions in background."""

    finished = Signal(object)
    error = Signal(str)

    def __init__(self, task_func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        try:
            result = self.task_func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))
