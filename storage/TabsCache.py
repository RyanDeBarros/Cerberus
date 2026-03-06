from pathlib import Path

import toml

from storage import FileSystemLocator
from graphics import FileTab

TABS_CACHE_PATH = FileSystemLocator.PERSISTENT_PATH / 'tabs'
TABS_CACHE_PATH.mkdir(exist_ok=True)

TABS_CACHE_MANIFEST_PATH = TABS_CACHE_PATH / 'manifest.toml'


class TabsCache:
	def __init__(self):
		self.d = {}

	@staticmethod
	def cache_path(file_number: int):
		return TABS_CACHE_PATH / f"{file_number}.txt"

	def load_and_clear(self) -> None:
		import AppContext
		if not TABS_CACHE_MANIFEST_PATH.exists():
			return

		with open(TABS_CACHE_MANIFEST_PATH, 'r') as f:
			self.d = toml.load(f)

		for manifest_entry in self.d['files']:
			file_number = manifest_entry['file_number']
			cache_path = self.cache_path(file_number)
			if 'file' in manifest_entry:
				filepath = manifest_entry['file']
				tab = FileTab(Path(filepath).resolve())
				if cache_path.exists():
					tab.force_load(cache_path.read_text())
				AppContext.main_window().add_file_tab(tab, add_to_ui=True)
			else:
				tab = FileTab(None)
				if cache_path.exists():
					tab.force_load(cache_path.read_text())
					AppContext.main_window().add_file_tab(tab, add_to_ui=True)
				else:
					pass  # TODO(2) log internal error

		self.d.clear()
		for file in TABS_CACHE_PATH.iterdir():
			if file.is_file():
				file.unlink()

	def cache_tab(self, tab: FileTab):
		manifest_entry = {}
		if 'files' not in self.d:
			self.d['files'] = []

		file_number = len(self.d['files'])
		manifest_entry['file_number'] = file_number
		cache_path = self.cache_path(file_number)

		if tab.filepath is None:
			if not tab.asterisk:
				return

			tab.save_to(cache_path)
		else:
			manifest_entry['file'] = tab.filepath.resolve().as_posix()
			if tab.asterisk:
				tab.save_to(cache_path)

		self.d['files'].append(manifest_entry)
		with open(TABS_CACHE_MANIFEST_PATH, 'w') as f:
			toml.dump(self.d, f)

		# TODO(1) test edge cases of persistent storage when multiple instances of Cerberus are running
