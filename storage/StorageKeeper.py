from pathlib import Path

import toml


class StorageKeeper:
	def __init__(self, obj, names: list[str], filename: str):
		self.obj = obj
		self.names = names
		self.path = self.data_path() / filename

		if self.path.exists():
			with open(self.path, 'r') as f:
				d = toml.load(f)
			for name in self.names:
				if name in d:
					setattr(self.obj, name, d[name])

	def store(self):
		self.path.parent.mkdir(parents=True, exist_ok=True)
		d = {}
		for name in self.names:
			d[name] = getattr(self.obj, name)
		with open(self.path, 'w') as f:
			toml.dump(d, f)

	@staticmethod
	def data_path():
		return Path('data').resolve()
