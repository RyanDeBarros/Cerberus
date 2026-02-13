from enum import Enum
from io import StringIO

from graphics import AppContext, Symbols


class EditCaseOption(Enum):
	Upper = 1
	Lower = 2
	Capitalize = 3
	Sentence = 4
	Title = 5


def set_upper_case():
	AppContext.insert_text(AppContext.selected_text().upper())


def set_lower_case():
	AppContext.insert_text(AppContext.selected_text().lower())


def set_capitalize_case():
	text = AppContext.selected_text()
	out = StringIO()
	on_first = True
	for c in text:
		if c in Symbols.word_separators:
			on_first = True
			out.write(c)
		elif on_first:
			out.write(c.upper())
			on_first = False
		else:
			out.write(c.lower())
	AppContext.insert_text(out.getvalue())


def set_sentence_case():
	text = AppContext.selected_text()
	out = StringIO()
	on_first = True
	for c in text:
		if c in Symbols.sentence_enders:
			on_first = True
			out.write(c)
		elif on_first:
			out.write(c.upper())
			if not c.isspace():
				on_first = False
		else:
			out.write(c.lower())  # TODO don't lowercase if whole word is 'i'
	AppContext.insert_text(out.getvalue())


def set_title_case():
	text = AppContext.selected_text()
	out = StringIO()
	i = 0
	# TODO first word in a sentence must always be capitalized
	while i < len(text):
		if text[i].lower() in Symbols.lowercase_alphabet:
			j = i + 1
			while j < len(text) and text[j].lower() in Symbols.lowercase_alphabet:
				j += 1
			word = text[i:j].lower()
			if word in Symbols.lowercase_nontitle_words:
				if word == 'i':
					out.write('I')
				else:
					out.write(word)
			else:
				out.write(word[0].upper())
				out.write(word[1:].lower())
			i = j
		else:
			out.write(text[i])
			i += 1
	AppContext.insert_text(out.getvalue())


def get_edit_case_action(option: EditCaseOption):
	match option:
		case EditCaseOption.Upper:
			return set_upper_case
		case EditCaseOption.Lower:
			return set_lower_case
		case EditCaseOption.Capitalize:
			return set_capitalize_case
		case EditCaseOption.Sentence:
			return set_sentence_case
		case EditCaseOption.Title:
			return set_title_case
