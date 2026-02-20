from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QMessageBox

from storage import PERSISTENT_DATA


class FileTab(QWidget):
	def __init__(self, filepath: Path | None):
		super().__init__()
		self.asterisk = False
		self.filepath = filepath

		self.vertical_layout = QVBoxLayout(self)
		self.text_area = QPlainTextEdit()
		self.vertical_layout.addWidget(self.text_area)
		self.text_area.textChanged.connect(self.text_changed)

		self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self.load()
		self.focus_text()

	def focus_text(self):
		self.text_area.setFocus()

	def text_changed(self):
		if not self.asterisk:
			self.asterisk = True
			self._set_tab_text()

	def on_save(self):
		if self.filepath is None and not self._init_filepath():
			return

		if self.asterisk:
			self.asterisk = False
			self._set_tab_text()
			self.filepath.write_text(self.text_area.toPlainText())

	def on_close(self):
		if not self.asterisk:
			return True
		mbox = QMessageBox(QMessageBox.Icon.Question, "Unsaved Changes", f"Do you want to save your changes to {self.raw_tabname()}?")
		yes = mbox.addButton("Yes", QMessageBox.ButtonRole.YesRole)
		no = mbox.addButton("No", QMessageBox.ButtonRole.NoRole)
		cancel = mbox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
		mbox.exec()
		if mbox.clickedButton() == yes:
			self.on_save()
		elif mbox.clickedButton() == no:
			pass
		elif mbox.clickedButton() == cancel:
			return False
		return True

	def load(self):
		if self.filepath is not None:
			self.text_area.setPlainText(self.filepath.read_text())  # TODO(3) don't open if file is too big - set maximum in settings
			self.asterisk = False

	def _set_tab_text(self):
		from graphics import AppContext
		index = AppContext.main_window().ui.tabWidget.indexOf(self)
		AppContext.main_window().ui.tabWidget.setTabText(index, self.tabname())

	def raw_tabname(self):
		return self.filepath.stem if self.filepath else "Untitled"

	def tabname(self):
		filename = self.raw_tabname()
		return filename if not self.asterisk else f"* {filename}"

	def _init_filepath(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename and filename != self.filepath:
			self.filepath = Path(filename).resolve()
			self._set_tab_text()
			return True
		else:
			return False
		# TODO(2) if overwriting an existing file (whether here or through some other action): check if that file is already open in Cerberus. If it is, then once that tab is focused, popup options to reload file or keep text content as unsaved changes. In fact, cache the last modified timestamp of currently open files so as to execute this popup when that timestamp changes (can be some kind of watchdog system or simply a separate thread that checks timestamps on a timer).

	def move_file(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename and filename != self.filepath:
			self.filepath.rename(filename)

	def save_as(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename:
			self.filepath = Path(filename).resolve()
			self.asterisk = True
			self.on_save()

	def save_copy(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename:
			Path(filename).resolve().write_text(self.text_area.toPlainText())
