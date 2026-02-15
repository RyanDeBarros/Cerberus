from io import StringIO

from graphics import AppContext
from storage import SYMBOLS


class FullIndex(int):
	def __add__(self, other):
		return FullIndex(super().__add__(other))

	def __sub__(self, other):
		return FullIndex(super().__sub__(other))


class SubIndex(int):
	def __add__(self, other):
		return SubIndex(super().__add__(other))

	def __sub__(self, other):
		return SubIndex(super().__sub__(other))


class TextSelection:
	def __init__(self, fulltext: str, position: FullIndex, anchor: FullIndex):
		self.fulltext = fulltext
		self.position = position
		self.anchor = anchor

	def full_index(self, i: SubIndex) -> FullIndex:
		if not self.is_in_range(i):
			raise IndexError()
		if self.position >= self.anchor:
			return FullIndex(self.anchor + i)
		else:
			return FullIndex(self.position + i)

	def char(self, i: FullIndex | SubIndex) -> str:
		if isinstance(i, SubIndex):
			i = self.full_index(i)
		return self.fulltext[i]

	def slice(self, i: FullIndex | SubIndex, j: FullIndex | SubIndex) -> str:
		if isinstance(i, SubIndex):
			i = self.full_index(i)
		if isinstance(j, SubIndex):
			j = self.full_index(j)
		return self.fulltext[i:j]

	def is_in_range(self, i: SubIndex) -> bool:
		return 0 <= i < abs(self.position - self.anchor)

	def selection_size(self) -> int:
		return abs(self.position - self.anchor)


class TextIterator:
	def __init__(self, index=SubIndex(0)):
		self.text = TextSelection(AppContext.all_text(), AppContext.text_cursor().position(), AppContext.text_cursor().anchor())
		self.index = index

	def valid(self):
		return self.text.is_in_range(self.index)

	def char(self):
		return self.text.char(self.index)

	def is_word_char(self, j: SubIndex | FullIndex | None = None):
		return self.text.char(self.index if j is None else j).lower() in SYMBOLS.lowercase_word_characters

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

		j = SubIndex(self.index - 1)
		while j >= 0 and self.is_word_char(j):
			j -= 1
		return self.index - j

	def left_subword(self):
		return self.text.slice(SubIndex(self.index - self.left_subword_len() + 1), self.index)

	# **aBc** => 2
	def right_subword_len(self):
		if not self.is_word_char():
			return 0

		j = SubIndex(self.index + 1)
		while j < self.text.selection_size() and self.is_word_char(j):
			j += 1
		return j - self.index

	def right_subword(self):
		return self.text.slice(self.index, SubIndex(self.index + self.right_subword_len()))

	# **aBc** => 2, 5
	def subword_range(self) -> tuple[SubIndex, SubIndex]:
		return SubIndex(self.index - self.left_subword_len() + 1), SubIndex(self.index + self.right_subword_len())

	def subword(self):
		l, r = self.subword_range()
		return self.text.slice(l, r)

	def is_first_letter_of_subword(self):
		return self.is_word_char() and (self.index == 0 or not self.is_word_char(SubIndex(self.index - 1)))

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
