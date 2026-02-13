from enum import Enum
from io import StringIO

from graphics import AppContext


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
		if c.isspace():  # TODO or other separator characters like '=', ':', etc. from Symbols
			on_first = True
			out.write(c)
		elif on_first:
			out.write(c.upper())
			on_first = False
		else:
			out.write(c.lower())
	AppContext.insert_text(out.getvalue())


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
