from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit


class FileTab(QWidget):
	def __init__(self, filename: str):
		super().__init__()
		self.asterisk = False
		self.filename = filename

		self.vertical_layout = QVBoxLayout(self)
		self.text_area = QPlainTextEdit()
		self.vertical_layout.addWidget(self.text_area)
		self.text_area.textChanged.connect(self.text_changed)

		self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self.text_area.setFocus()

	def text_changed(self):
		if not self.asterisk:
			self.asterisk = True
			self._set_tab_text(f"* {self.filename}")

	def on_save(self):
		if self.asterisk:
			self.asterisk = False
			self._set_tab_text(self.filename)

	def _set_tab_text(self, text):
		from graphics import AppContext
		index = AppContext.main_window().ui.tabWidget.indexOf(self)
		AppContext.main_window().ui.tabWidget.setTabText(index, text)
