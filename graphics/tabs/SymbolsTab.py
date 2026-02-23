from graphics import EditorTab

from storage import StorageKeeper, Symbols


class SymbolsTab(EditorTab):
	def __init__(self):
		super().__init__("Settings - Symbols")
		self.symbols = Symbols()
		self.storage = StorageKeeper(self.symbols, [
			"whitespace",
			"sentence_enders",
			"lowercase_word_characters",
			"lowercase_nontitle_words",
			"lowercase_alphabet",
		], 'symbols.toml')
		self.storage.load()

	def load(self):
		self.storage.load()

	def dump(self):
		self.storage.dump()
