import os
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QWidget

from .StorageKeeper import StorageKeeper

PERSISTENT_DATA_PATH = Path('data/persistent.toml')


@dataclass
class PersistentData:
	file_dialog_dir: str = ""

	def __init__(self):
		self.storage = StorageKeeper(self, [
			"file_dialog_dir",
		], 'persistent.toml')

	def _store(self):
		self.storage.store()

	def get_open_filenames(self, widget: QWidget, ext_filter: str = "Text Files (*.txt *.md *.log);; All Files (*)"):
		filenames, _ = QFileDialog.getOpenFileNames(widget, "Open File", self.file_dialog_dir, ext_filter)
		if filenames:
			self.file_dialog_dir = os.path.dirname(filenames[0])
			self._store()
			return filenames
		else:
			return []

	def get_save_filename(self, widget: QWidget, ext_filter: str = ""):
		filename, _ = QFileDialog.getSaveFileName(widget, "Save File", self.file_dialog_dir, ext_filter)
		if filename:
			self.file_dialog_dir = os.path.dirname(filename)
			self._store()
		return filename


PERSISTENT_DATA = PersistentData()
