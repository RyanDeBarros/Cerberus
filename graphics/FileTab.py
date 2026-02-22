from pathlib import Path
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QPlainTextEdit, QMessageBox

from graphics import TextArea, AbstractTab
from storage import PERSISTENT_DATA


class FileTab(AbstractTab):
	def __init__(self, filepath: Path | None):
		super().__init__()
		self.filepath = filepath

		self.vertical_layout = QVBoxLayout(self)
		self.text_edit = QPlainTextEdit()
		self.vertical_layout.addWidget(self.text_edit)
		self.text_edit.textChanged.connect(self.text_changed)
		self.text_area = TextArea(self.text_edit)

		self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self.load()
		self.focus_text()

	def on_added(self):
		self._on_filepath_changed()

	def _on_filepath_changed(self):
		fullpath = self.filepath.as_posix() if self.filepath else "Untitled"
		self.setToolTip(fullpath if not self.asterisk else f"* {fullpath}")

	def focus_text(self):
		self.text_edit.setFocus()

	def text_changed(self):
		if not self.asterisk:
			self.set_asterisk(True)

	@override
	def on_save(self):
		if self.filepath is None and not self._init_filepath():
			return

		if self.asterisk:
			self.set_asterisk(False)
			self.filepath.write_text(self.text_edit.toPlainText())

	def load(self):
		if self.filepath is not None:
			self.text_edit.setPlainText(self.filepath.read_text())  # TODO(2) don't open if file is too big - set maximum in settings
			self.set_asterisk(False)

	@override
	def raw_tabname(self):
		return self.filepath.name if self.filepath else "Untitled"

	def _init_filepath(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename and filename != self.filepath:
			self.filepath = Path(filename).resolve()
			self._on_filepath_changed()
			self._set_tab_text()
			return True
		else:
			return False
		# TODO(1) if overwriting an existing file (whether here or through some other action): check if that file is already open in Cerberus. If it is, then once that tab is focused, popup options to reload file or keep text content as unsaved changes. In fact, cache the last modified timestamp of currently open files so as to execute this popup when that timestamp changes (can be some kind of watchdog system or simply a separate thread that checks timestamps on a timer).

	def move_file(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename and filename != self.filepath:
			self.filepath.rename(filename)

	def save_as(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename:
			self.filepath = Path(filename).resolve()
			self._on_filepath_changed()
			self.asterisk = True
			self.on_save()

	def save_copy(self):
		filename = PERSISTENT_DATA.get_save_filename(self)
		if filename:
			Path(filename).resolve().write_text(self.text_edit.toPlainText())

	def on_delete(self):
		mbox = QMessageBox(QMessageBox.Icon.Warning, "Confirm Delete File", f"Are you sure you want to delete {self.filepath if self.filepath else "Untitled"}?")
		yes = mbox.addButton("Yes", QMessageBox.ButtonRole.YesRole)
		cancel = mbox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
		mbox.setDefaultButton(cancel)
		mbox.exec()
		if mbox.clickedButton() == yes:
			if self.filepath:
				self.filepath.unlink()
			return True
		else:
			return False
