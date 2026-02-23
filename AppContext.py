from typing import TYPE_CHECKING, Optional

from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
	from graphics import TextArea
	from graphics import MainWindow
	from storage import Symbols
	from storage import PersistentData

MAIN_WINDOW: Optional["MainWindow"] = None
PERSISTENT_DATA: Optional["PersistentData"] = None


def run_app():
	app = QApplication([])

	from graphics import MainWindow
	global MAIN_WINDOW
	MAIN_WINDOW = MainWindow()

	from storage import PersistentData
	global PERSISTENT_DATA
	PERSISTENT_DATA = PersistentData()

	MAIN_WINDOW.show()
	app.exec()


def main_window() -> "MainWindow":
	return MAIN_WINDOW


def text_area() -> "TextArea":
	return main_window().get_file_tab().text_area


def symbols() -> "Symbols":
	return main_window().symbols_tab.symbols


def persistent() -> "PersistentData":
	return PERSISTENT_DATA
