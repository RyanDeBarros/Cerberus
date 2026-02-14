from dataclasses import dataclass
from pathlib import Path

from .StorageKeeper import StorageKeeper

PERSISTENT_DATA_PATH = Path('data/persistent.toml')


@dataclass
class PersistentData:
	file_dialog_dir: str = ""

	def __init__(self):
		self.storage = StorageKeeper(self, [
			"file_dialog_dir",
		], Path('data/persistent.toml'))

	def store(self):
		self.storage.store()


PERSISTENT_DATA = PersistentData()
