from contextlib import contextmanager
from enum import Enum
from io import StringIO

from graphics import AppContext
from processing.EarlyExit import EarlyExitAtChar
from processing.TextIterator import TextIterator  # TODO why is it importing TextIterator module and not class?
from storage import SYMBOLS


class EditCaseOption(Enum):
	Upper = 1
	Lower = 2
	Capitalize = 3
	Sentence = 4
	Title = 5


@contextmanager
def restore_cursor():
	cursor = AppContext.text_cursor()
	position = cursor.position()
	anchor = cursor.anchor()
	yield cursor
	AppContext.text_area().setFocus()
	cursor = AppContext.text_cursor()
	cursor.setPosition(anchor)
	cursor.setPosition(position, cursor.MoveMode.KeepAnchor)
	AppContext.set_text_cursor(cursor)


def set_upper_case():
	AppContext.insert_text(AppContext.selected_text().upper())


def set_lower_case():
	AppContext.insert_text(AppContext.selected_text().lower())


def set_capitalize_case():
	out = StringIO()
	it = TextIterator()
	while it.valid():
		if it.is_word_char():
			if it.is_first_letter_of_word():
				it.write_char_upper(out)
			else:
				it.write_up_to_next_subword(out)
		else:
			it.write_char(out)
	AppContext.insert_text(out.getvalue())


def set_sentence_case():
	out = StringIO()
	it = TextIterator()
	early_exit = EarlyExitAtChar(it, ''.join(SYMBOLS.sentence_enders))
	on_first_word = it.valid() and it.is_first_word_of_sentence()
	while it.valid():
		if it.char() in SYMBOLS.sentence_enders:
			it.write_char(out)
			on_first_word = True
			continue

		if it.is_word_char():
			if on_first_word:
				on_first_word = False
				if it.is_first_letter_of_word():
					it.write_char_upper(out)
					continue
			elif it.word() == 'i':
				it.write_char_upper(out)
				continue

		it.write_up_to_next_subword(out, early_exit)
	AppContext.insert_text(out.getvalue())


def set_title_case():
	text = AppContext.selected_text()
	out = StringIO()
	i = 0
	# TODO first word in a sentence must always be capitalized
	while i < len(text):
		if text[i].lower() in SYMBOLS.lowercase_alphabet:
			j = i + 1
			while j < len(text) and text[j].lower() in SYMBOLS.lowercase_alphabet:
				j += 1
			word = text[i:j].lower()
			if word in SYMBOLS.lowercase_nontitle_words:
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


def get_wrapped_edit_case_action(action):
	def f():
		with restore_cursor():
			action()
	return f


def get_edit_case_action(option: EditCaseOption):
	match option:
		case EditCaseOption.Upper:
			return get_wrapped_edit_case_action(set_upper_case)
		case EditCaseOption.Lower:
			return get_wrapped_edit_case_action(set_lower_case)
		case EditCaseOption.Capitalize:
			return get_wrapped_edit_case_action(set_capitalize_case)
		case EditCaseOption.Sentence:
			return get_wrapped_edit_case_action(set_sentence_case)
		case EditCaseOption.Title:
			return get_wrapped_edit_case_action(set_title_case)
