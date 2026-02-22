from typing import TYPE_CHECKING, Optional

from PySide6.QtWidgets import QApplication

from graphics import TextArea

if TYPE_CHECKING:
	from graphics.MainWindow import MainWindow

MAIN_WINDOW: Optional["MainWindow"] = None


def run_app():
	global MAIN_WINDOW
	app = QApplication([])
	from graphics import MainWindow
	MAIN_WINDOW = MainWindow()
	MAIN_WINDOW.show()
	app.exec()


def main_window() -> "MainWindow":
	return MAIN_WINDOW


def text_area() -> TextArea:
	return MAIN_WINDOW.get_tab().text_area
