from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication

from graphics import MainWindow

MAIN_WINDOW: MainWindow | None = None

def run_app():
	global MAIN_WINDOW
	app = QApplication([])
	MAIN_WINDOW = MainWindow()
	MAIN_WINDOW.show()
	app.exec()

def main_window():
	return MAIN_WINDOW

def text_area():
	return MAIN_WINDOW.ui.textArea

def all_text():
	return text_area().toPlainText()

def text_cursor():
	return text_area().textCursor()

def set_text_cursor(cursor: QTextCursor):
	return text_area().setTextCursor(cursor)

def selected_text():
	return text_cursor().selectedText().replace('\u2029', '\n')

def insert_text(text: str):
	text_cursor().insertText(text)
