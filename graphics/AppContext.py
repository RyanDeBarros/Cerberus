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
