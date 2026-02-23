from typing import override

from graphics import EditorTab

from storage import StorageKeeper, Symbols
from ui import Ui_SymbolsSettings


class Strings:
	sentence_enders = "sentence_enders"
	lowercase_nontitle_words = "lowercase_nontitle_words"

STRINGS = Strings()


class SymbolsTab(EditorTab):
	def __init__(self):
		super().__init__("Settings - Symbols")
		self.symbols = Symbols()
		self.scratch_symbols = Symbols()
		self.storage = StorageKeeper(self.symbols, [
			STRINGS.sentence_enders,
			STRINGS.lowercase_nontitle_words,
		], 'symbols.toml')
		self.load()

		self.ui = Ui_SymbolsSettings()
		self.ui.setupUi(self)

		self.ui.openSentenceEnders.clicked.connect(self.open_sentence_enders)
		self.rvtSentenceEnders = self.revert_button(self.ui.revertSentenceEnders, STRINGS.sentence_enders)
		self.ui.openNonTitleWords.clicked.connect(self.open_non_title_words)
		self.rvtNonTitleWords = self.revert_button(self.ui.revertNonTitleWords, STRINGS.lowercase_nontitle_words)

	@override
	def load(self):
		self.storage.load()
		self.storage.dump_to(self.scratch_symbols)

	@override
	def dump(self):
		self.storage.load_from(self.scratch_symbols)
		self.storage.dump()

	@override
	def storage_keeper(self) -> StorageKeeper:
		return self.storage

	@override
	def data(self):
		return self.symbols

	@override
	def scratch_data(self):
		return self.scratch_symbols

	def open_sentence_enders(self):
		self.open_strings_set_dialog(STRINGS.sentence_enders, self.rvtSentenceEnders)

	def open_non_title_words(self):
		self.open_strings_set_dialog(STRINGS.lowercase_nontitle_words, self.rvtNonTitleWords, self.strings_list_to_lower_op)
