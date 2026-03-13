from contextlib import contextmanager
from typing import TypeVar, Generator

from PySide6.QtWidgets import QWidget


QWidgetSubClass = TypeVar("T", bound=QWidget)

@contextmanager
def block_signals(ui: QWidgetSubClass) -> Generator[QWidgetSubClass, None, None]:
	b = ui.signalsBlocked()
	ui.blockSignals(True)
	yield ui
	ui.blockSignals(b)
