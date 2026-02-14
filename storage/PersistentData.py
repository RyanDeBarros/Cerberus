from dataclasses import dataclass
from pathlib import Path

import toml

PERSISTENT_DATA_PATH = Path('data/persistent.toml')


@dataclass
class PersistentData:
	file_dialog_dir: str = ""

	def load(self):
		if PERSISTENT_DATA_PATH.exists():
			with open(PERSISTENT_DATA_PATH, 'r') as f:
				self.__dict__.update(toml.load(f))

	def save(self):
		PERSISTENT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
		with open(PERSISTENT_DATA_PATH, 'w') as f:
			toml.dump(self.__dict__, f)


PERSISTENT_DATA = PersistentData()
