from pathlib import Path
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QPlainTextEdit, QMessageBox

import AppContext
from graphics import TextArea, AbstractTab


class FileTab(AbstractTab):
	def __init__(self, filepath: Path | None):
		super().__init__()
		self.filepath = filepath
		if self.filepath is not None and self.filepath.exists():
			self.timestamp = self.file_modified_timestamp()
		else:
			self.timestamp = -1
		self.popup_no_exist = True
		self.external_timestamp: int | None = None

		self.vertical_layout = QVBoxLayout(self)
		self.text_edit = QPlainTextEdit()
		self.vertical_layout.addWidget(self.text_edit)
		self.text_edit.textChanged.connect(self.text_changed)
		self.text_area = TextArea(self.text_edit)

		self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self.load()
		self.focus()

	def on_added(self):
		self._on_filepath_changed()

	def _on_filepath_changed(self):
		fullpath = self.filepath.as_posix() if self.filepath else "Untitled"
		self.setToolTip(fullpath if not self.asterisk else f"* {fullpath}")

	def focus(self):
		self.check_for_external_change(from_focus=True)
		self.text_edit.setFocus()

	def text_changed(self):
		if not self.asterisk:
			self.set_asterisk(True)

	@override
	def on_save(self):
		if self.filepath is None:
			filename = AppContext.persistent().get_save_filename(self)
			if not filename:
				return

			self.filepath = Path(filename).resolve()
			self._on_filepath_changed()
			self._set_tab_text()
			self.timestamp = self.file_modified_timestamp()

		if self.asterisk:
			self.check_for_external_change(from_focus=False)
			self.set_asterisk(False)
			self._save_to(self.filepath)

	@override
	def load(self):
		if self.filepath is not None:
			if self.filepath.exists():
				self.text_area.set_text(self.filepath.read_text())  # TODO(2) don't open if file is too big - set maximum in settings
				self.set_asterisk(False)
				self.focus()
			else:
				pass  # TODO(2) handle case?

	@override
	def raw_tabname(self):
		return self.filepath.name if self.filepath else "Untitled"

	def file_modified_timestamp(self) -> int | None:
		return self.filepath.stat().st_mtime if self.filepath and self.filepath.exists() else None

	def move_file(self):
		filename = AppContext.persistent().get_save_filename(self)
		if filename and filename != self.filepath:
			self.filepath.rename(filename)

	def save_as(self):
		filename = AppContext.persistent().get_save_filename(self)
		if filename:
			self.filepath = Path(filename).resolve()
			self._on_filepath_changed()
			self.asterisk = True
			self.on_save()

	def save_copy(self):
		filename = AppContext.persistent().get_save_filename(self)
		if filename:
			self._save_to(Path(filename))

	def _save_to(self, file: Path):
		file.write_text(self.text_edit.toPlainText())

	def on_delete(self):
		mbox = QMessageBox(QMessageBox.Icon.Warning, "Confirm Delete File", f"Are you sure you want to delete {self.filepath if self.filepath else "Untitled"}?")
		yes = mbox.addButton("Yes", QMessageBox.ButtonRole.YesRole)
		cancel = mbox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
		mbox.setDefaultButton(cancel)
		mbox.exec()
		if mbox.clickedButton() == yes:
			if self.filepath and self.filepath.exists():
				self.filepath.unlink()
			return True
		else:
			return False

	# TODO(1) Call check_for_external_change using some kind of watchdog system or simply a separate thread with a timer *while tab is focused*.
	def check_for_external_change(self, from_focus: bool):
		if self.filepath is None or not AppContext.main_window().tab_is_selected(self):
			return

		file_modified_timestamp = self.file_modified_timestamp()
		if not self.filepath.exists():
			if from_focus and self.popup_no_exist:
				mbox = QMessageBox(QMessageBox.Icon.Information, "File doesn't exist", f"{self.filepath} was removed externally, and no longer exists.")
				mbox.exec()
				self.popup_no_exist = False
			self.set_asterisk(True)
			self.external_timestamp = None
		elif file_modified_timestamp > self.timestamp or (self.external_timestamp is not None and file_modified_timestamp > self.external_timestamp):
			self.popup_no_exist = True
			if self.external_timestamp is None or file_modified_timestamp > self.external_timestamp:
				self.external_timestamp = file_modified_timestamp

				mbox = QMessageBox(QMessageBox.Icon.Question, "File was modified externally", f"{self.filepath} was modified externally - what should Cerberus do?")
				reload = mbox.addButton("Reload from disk", QMessageBox.ButtonRole.ApplyRole)
				keep_changes = mbox.addButton("Keep unsaved changes", QMessageBox.ButtonRole.RejectRole)
				mbox.setDefaultButton(keep_changes)
				mbox.exec()
				if mbox.clickedButton() == reload:
					self.load()
				else:
					self.set_asterisk(True)
		else:
			self.popup_no_exist = True
			self.external_timestamp = None
