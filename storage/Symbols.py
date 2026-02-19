from dataclasses import dataclass
from pathlib import Path

from .StorageKeeper import StorageKeeper

SYMBOLS_DATA_PATH = Path('data/symbols.toml')


# TODO(2) app settings to configure Symbols
@dataclass
class Symbols:
	whitespace = [' ', '\t', '\r', '\n']
	sentence_enders = ['.', '!', '?']
	lowercase_word_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2',
								 '3', '4', '5', '6', '7', '8', '9', '_']
	lowercase_nontitle_words = ['a', 'an', 'in', 'is', 'it', 'of', 'on', 'to', 'the']
	lowercase_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

	def __init__(self):
		self.storage = StorageKeeper(self, [
			"whitespace",
			"sentence_enders",
			"lowercase_word_characters",
			"lowercase_nontitle_words",
			"lowercase_alphabet",
		], Path('data/symbols.toml'))

	def store(self):
		self.storage.store()


SYMBOLS = Symbols()
