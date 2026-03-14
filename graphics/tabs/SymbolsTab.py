from dataclasses import dataclass, field
from typing import override

from graphics import EditorTab

from ui import Ui_SymbolsSettings


@dataclass
class Symbols:
	whitespace: set[str] = field(default_factory=lambda: {' ', '\t', '\r', '\n'})
	sentence_enders: set[str] = field(default_factory=lambda: {'.', '!', '?'})
	lowercase_word_characters: set[str] = field(
		default_factory=lambda: {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2',
								 '3', '4', '5', '6', '7', '8', '9', '_'})
	lowercase_nontitle_words: set[str] = field(default_factory=lambda: {'a', 'an', 'in', 'is', 'it', 'of', 'on', 'to', 'the'})
	lowercase_alphabet: set[str] = field(
		default_factory=lambda: {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'})


class Strings:
	sentence_enders = "sentence_enders"
	lowercase_nontitle_words = "lowercase_nontitle_words"


STRINGS = Strings()


class SymbolsTab(EditorTab):
	def __init__(self):
		self.symbols = Symbols()
		self.scratch_symbols = Symbols()
		super().__init__("Settings - Symbols", 'symbols.toml')

		self.ui = Ui_SymbolsSettings()
		self.ui.setupUi(self)

		self.ui.openSentenceEnders.clicked.connect(self.open_sentence_enders)
		self.revert_sentence_enders = self.revert_button(self.ui.revertSentenceEnders, self.strings().sentence_enders)
		self.ui.openNonTitleWords.clicked.connect(self.open_non_title_words)
		self.revert_non_title_words = self.revert_button(self.ui.revertNonTitleWords, self.strings().lowercase_nontitle_words)

		self.load()

	@override
	def data(self):
		return self.symbols

	@override
	def scratch_data(self):
		return self.scratch_symbols

	@override
	def revert_buttons(self):
		return [self.revert_sentence_enders, self.revert_non_title_words]

	@override
	def strings(self):
		return STRINGS

	@override
	def render_scratch_ui(self, name: str):
		pass

	def open_sentence_enders(self):
		self.open_strings_set_dialog(self.strings().sentence_enders, self.revert_sentence_enders)

	def open_non_title_words(self):
		self.open_strings_set_dialog(self.strings().lowercase_nontitle_words, self.revert_non_title_words, self.strings_list_to_lower_op)
