from copy import deepcopy
from typing import override

from graphics import RevertButton, EditorTab, DynamicStringList

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
		# self.rvtSentenceEnders = RevertButton(self.ui.revertSentenceEnders, self.rvt_get_temp_value(self.symbols, STRINGS.sentence_enders),
		# 									  self.rvt_set_temp_value(STRINGS.sentence_enders), self.rvt_get_default_value(self.storage, STRINGS.sentence_enders))

		self.ui.openNonTitleWords.clicked.connect(self.open_non_title_words)
		# self.rvtNonTitleWords = RevertButton(self.ui.revertNonTitleWords, self.rvt_get_temp_value(self.symbols, STRINGS.lowercase_nontitle_words),
		# 									  self.rvt_set_temp_value(STRINGS.lowercase_nontitle_words), self.rvt_get_default_value(self.storage, STRINGS.lowercase_nontitle_words))

	@override
	def load(self):
		self.storage.load()
		self.scratch_symbols = deepcopy(self.symbols)

	@override
	def dump(self):
		self.symbols = deepcopy(self.scratch_symbols)
		self.storage.dump()

	def open_sentence_enders(self):
		new_strings, modified = DynamicStringList.dialog(sorted(self.scratch_symbols.sentence_enders))
		if not modified:
			return

		# self.rvtSentenceEnders.value_changed()
		new_strings = set(new_strings)

		self.scratch_symbols.sentence_enders = new_strings
		if self.scratch_symbols.sentence_enders != self.symbols.sentence_enders:
			self.set_asterisk(True)

	def open_non_title_words(self):
		new_strings, modified = DynamicStringList.dialog(sorted(self.scratch_symbols.lowercase_nontitle_words))
		if not modified:
			return

		# self.rvtNonTitleWords.value_changed()
		s = set()
		for string in new_strings:
			s.add(string.lower())
		new_strings = s

		self.scratch_symbols.lowercase_nontitle_words = new_strings
		if self.scratch_symbols.lowercase_nontitle_words != self.symbols.lowercase_nontitle_words:
			self.set_asterisk(True)
