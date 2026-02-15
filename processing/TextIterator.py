from io import StringIO

from graphics import AppContext
from storage import SYMBOLS


class TextIterator:
	def __init__(self, fulltext: str | None = None, subtext: str | None = None, index=0):  # TODO pass subtext as subrange instead
		self.fulltext = fulltext if fulltext is not None else AppContext.all_text()
		self.subtext = subtext if subtext is not None else AppContext.selected_text()
		self.index = index

	def valid(self):
		return 0 <= self.index < len(self.subtext)

	def char(self):
		return self.subtext[self.index]

	def is_word_char(self, j: int | None = None):
		return self.subtext[self.index if j is None else j].lower() in SYMBOLS.lowercase_word_characters  # TODO differentiate between subtext indexing and fulltext indexing

	def to_next_char(self):
		self.index += 1

	def write_char(self, out: StringIO):
		out.write(self.char())
		self.to_next_char()

	def write_char_upper(self, out: StringIO):
		out.write(self.char().upper())
		self.to_next_char()

	def write_char_lower(self, out: StringIO):
		out.write(self.char().lower())
		self.to_next_char()

	# **aBc** => 2
	def left_subword_len(self) -> int:
		if not self.is_word_char():
			return 0

		j = self.index - 1
		while j >= 0 and self.is_word_char(j):
			j -= 1
		return self.index - j

	def left_subword(self):
		return self.subtext[self.index - self.left_subword_len() + 1: self.index]

	# **aBc** => 2
	def right_subword_len(self):
		if not self.is_word_char():
			return 0

		j = self.index + 1
		while j < len(self.subtext) and self.is_word_char(j):
			j += 1
		return j - self.index

	def right_subword(self):
		return self.subtext[self.index: self.index + self.right_subword_len()]

	# **aBc** => 2, 5
	def subword_range(self):
		return self.index - self.left_subword_len() + 1, self.index + self.right_subword_len()

	def subword(self):
		l, r = self.subword_range()
		return self.subtext[l:r]

	def is_first_letter_of_subword(self):
		return self.is_word_char() and (self.index == 0 or not self.is_word_char(self.index - 1))

	# TODO fullword variants of subword methods

	def distance_to_next_word(self):
		base = self.index
		self.index += self.right_subword_len()
		while self.valid() and self.is_word_char():
			self.index += 1
		distance = self.index - base
		self.index = base
		return distance

	def to_next_word(self):
		self.index += self.distance_to_next_word()

	def write_up_to_next_word(self, out: StringIO):
		d = self.distance_to_next_word()
		while d > 0:
			out.write(self.char())
			self.to_next_char()
			d -= 1
