from typing import override

from PySide6.QtWidgets import QDialog

from graphics import EditorTab, DynamicStringList

from storage import StorageKeeper, Symbols
from ui import Ui_SymbolsSettings


class SymbolsTab(EditorTab):
	def __init__(self):
		super().__init__("Settings - Symbols")
		self.symbols = Symbols()
		self.storage = StorageKeeper(self.symbols, [
			"sentence_enders",
			"lowercase_nontitle_words",
		], 'symbols.toml')
		self.storage.load()

		self.ui = Ui_SymbolsSettings()
		self.ui.setupUi(self)

		self.ui.openSentenceEnders.clicked.connect(self.open_sentence_enders)
		self.ui.openNonTitleWords.clicked.connect(self.open_non_title_words)

	@override
	def load(self):
		self.storage.load()

	@override
	def dump(self):
		self.storage.dump()

	def open_sentence_enders(self):
		DynamicStringList.dialog(self.symbols.sentence_enders)
		pass  # TODO(1)

	def open_non_title_words(self):
		DynamicStringList.dialog(self.symbols.lowercase_nontitle_words)
		pass  # TODO(1)
