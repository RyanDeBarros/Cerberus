from pathlib import Path

import toml


class StorageKeeper:
	def __init__(self, obj, names: list[str], filename: str):
		self.obj = obj
		self.names = names
		self.path = Path('data').resolve() / filename  # TODO(3) use app data path

		self.default_path = Path('default_data').resolve() / filename
		assert self.default_path.exists()
		with open(self.default_path, 'r') as f:
			self.defaults = toml.load(f)

	def load(self):
		if self.path.exists():
			with open(self.path, 'r') as f:
				d = toml.load(f)
			for name in self.names:
				if name in d:
					setattr(self.obj, name, d[name])

	def load_attr(self, name):
		if self.path.exists():
			with open(self.path, 'r') as f:
				d = toml.load(f)
			if name in d:
				setattr(self.obj, name, d[name])

	def dump(self):
		self.path.parent.mkdir(parents=True, exist_ok=True)
		d = {}
		for name in self.names:
			d[name] = getattr(self.obj, name)
		with open(self.path, 'w') as f:
			toml.dump(d, f)

	def load_defaults(self):
		for name in self.names:
			if name in self.defaults:
				setattr(self.obj, name, self.defaults[name])

	def load_default_attr(self, name):
		if name in self.defaults:
			setattr(self.obj, name, self.defaults[name])

	def get_default_attr(self, name):
		return self.defaults.get(name)
