from enum import Enum

from graphics import text_area


class EditCaseOption(Enum):
	Upper = 1
	Lower = 2
	Capitalize = 3
	Sentence = 4
	Title = 5

def set_upper_case():
	cursor = text_area().textCursor()
	cursor.insertText(cursor.selectedText().upper())

def set_lower_case():
	cursor = text_area().textCursor()
	cursor.insertText(cursor.selectedText().lower())

def set_capitalize_case():
	pass  # TODO

def set_sentence_case():
	pass  # TODO

def set_title_case():
	pass  # TODO

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
