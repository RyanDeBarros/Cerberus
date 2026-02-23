class Symbols:
	whitespace: set[str] = {' ', '\t', '\r', '\n'}
	sentence_enders: set[str] = {'.', '!', '?'}
	lowercase_word_characters: set[str] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0',
										   '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'}
	lowercase_nontitle_words: set[str] = {'a', 'an', 'in', 'is', 'it', 'of', 'on', 'to', 'the'}
	lowercase_alphabet: set[str] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
