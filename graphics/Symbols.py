from dataclasses import dataclass


# TODO app settings to configure Symbols
@dataclass
class Symbols:
	whitespace = [' ', '\t', '\r', '\n']
	sentence_enders = ['.', '!', '?']
	word_separators = [' ', '\t', '\r', '\n', '.', '!', '?', '\'', '"', '`', ',', ':', ';', '=', '~']
	lowercase_nontitle_words = ['a', 'an', 'of', 'the']
	lowercase_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
