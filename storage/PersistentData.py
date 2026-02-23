import os
from dataclasses import dataclass

from PySide6.QtWidgets import QFileDialog, QWidget

from .StorageKeeper import StorageKeeper


@dataclass
class PersistentData:
	file_dialog_dir: str = ""

	def __init__(self):
		self.storage = StorageKeeper(self, [
			"file_dialog_dir",
		], 'persistent.toml')
		self.storage.load()

	def get_open_filenames(self, widget: QWidget, ext_filter: str = "Text Files (*.txt *.md *.log);; All Files (*)"):
		filenames, _ = QFileDialog.getOpenFileNames(widget, "Open File", self.file_dialog_dir, ext_filter)
		if filenames:
			self.file_dialog_dir = os.path.dirname(filenames[0])
			self.storage.dump()
			return filenames
		else:
			return []

	def get_save_filename(self, widget: QWidget, ext_filter: str = ""):
		filename, _ = QFileDialog.getSaveFileName(widget, "Save File", self.file_dialog_dir, ext_filter)
		if filename:
			self.file_dialog_dir = os.path.dirname(filename)
			self.storage.dump()
		return filename
