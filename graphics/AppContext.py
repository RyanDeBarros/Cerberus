from typing import TYPE_CHECKING, Optional

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QPlainTextEdit

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


def text_area() -> QPlainTextEdit:
	return MAIN_WINDOW.get_tab().text_area


def all_text() -> str:
	return text_area().toPlainText()


def text_cursor() -> QTextCursor:
	return text_area().textCursor()


def set_text_cursor(cursor: QTextCursor) -> None:
	text_area().setTextCursor(cursor)


def selected_text() -> str:
	return text_cursor().selectedText().replace('\u2029', '\n')


def insert_text(text: str) -> None:
	text_cursor().insertText(text)
