from enum import Enum
from io import StringIO

from graphics import AppContext
from processing import TextIterator, EarlyExitAtChar, CharacterCase, restore_selection
from storage import SYMBOLS


class EditCaseOption(Enum):
	Upper = 1
	Lower = 2
	Capitalize = 3
	Sentence = 4
	Title = 5


def set_upper_case():
	text_area = AppContext.text_area()
	text_area.insert_text(text_area.selected_text().upper())


def set_lower_case():
	text_area = AppContext.text_area()
	text_area.insert_text(text_area.selected_text().lower())


def set_capitalize_case():
	out = StringIO()
	it = TextIterator()
	while it.valid():
		if it.is_word_char():
			if it.is_first_letter_of_word():
				it.write_char(out, CharacterCase.UPPER)
			else:
				it.write_up_to_next_subword(out)
		else:
			it.write_char(out)
	AppContext.text_area().insert_text(out.getvalue())


def set_sentence_case():
	out = StringIO()
	it = TextIterator()
	early_exit = EarlyExitAtChar(it, ''.join(SYMBOLS.sentence_enders))
	on_first_word = it.is_first_word_of_sentence()
	while it.valid():
		if it.char() in SYMBOLS.sentence_enders:
			it.write_char(out)
			on_first_word = True
			continue

		if it.is_word_char():
			if on_first_word:
				on_first_word = False
				if it.is_first_letter_of_word():
					it.write_char(out, CharacterCase.UPPER)
					continue
			elif it.word().lower() == 'i':
				it.write_char(out, CharacterCase.UPPER)
				continue

		it.write_up_to_next_subword(out, early_exit=early_exit, case=CharacterCase.LOWER)
	AppContext.text_area().insert_text(out.getvalue())


def set_title_case():
	out = StringIO()
	it = TextIterator()
	early_exit = EarlyExitAtChar(it, ''.join(SYMBOLS.sentence_enders))

	if it.valid() and not it.is_first_letter_of_word():
		it.write_chars(out, it.right_subword_len(), CharacterCase.LOWER)
		on_first_word = False
	else:
		on_first_word = it.is_first_word_of_sentence()

	while it.valid():
		if it.char() in SYMBOLS.sentence_enders:
			it.write_char(out)
			on_first_word = True
		elif it.is_word_char():
			case = CharacterCase.LOWER
			if on_first_word:
				on_first_word = False
				case = CharacterCase.CAPITALIZE
			else:
				word = it.word()
				if word.lower() not in SYMBOLS.lowercase_nontitle_words or word.lower() == 'i':
					case = CharacterCase.CAPITALIZE
			it.write_chars(out, it.right_subword_len(), case)
		else:
			it.write_up_to_next_subword(out, early_exit=early_exit, case=CharacterCase.LOWER)

	AppContext.text_area().insert_text(out.getvalue())


def get_wrapped_edit_case_action(action):
	def f():
		if AppContext.main_window().has_tab():
			with restore_selection():
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
