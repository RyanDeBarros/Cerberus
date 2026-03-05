from typing import TYPE_CHECKING, Optional

from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
	from graphics import TextArea
	from graphics import MainWindow
	from storage import Symbols
	from storage import PersistentData

_MAIN_WINDOW: Optional["MainWindow"] = None
_PERSISTENT_DATA: Optional["PersistentData"] = None


def run_app():
	app = QApplication([])

	from graphics import MainWindow
	global _MAIN_WINDOW
	_MAIN_WINDOW = MainWindow()

	from storage import PersistentData
	global _PERSISTENT_DATA
	_PERSISTENT_DATA = PersistentData()

	_MAIN_WINDOW.show()
	app.exec()


def main_window() -> "MainWindow":
	return _MAIN_WINDOW


def text_area() -> "TextArea":
	return main_window().get_file_tab().text_area


def symbols() -> "Symbols":
	return main_window().symbols_tab.symbols


def persistent() -> "PersistentData":
	return _PERSISTENT_DATA
