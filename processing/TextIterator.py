from abc import ABC, abstractmethod
from enum import Enum
from io import StringIO

from graphics import AppContext
from storage import SYMBOLS


class FullIndex(int):
	def __add__(self, other):
		if isinstance(other, SubIndex):
			raise TypeError()
		return FullIndex(super().__add__(other))

	def __sub__(self, other):
		if isinstance(other, SubIndex):
			raise TypeError()
		return FullIndex(super().__sub__(other))


class SubIndex(int):
	def __add__(self, other):
		if isinstance(other, FullIndex):
			raise TypeError()
		return SubIndex(super().__add__(other))

	def __sub__(self, other):
		if isinstance(other, FullIndex):
			raise TypeError()
		return SubIndex(super().__sub__(other))


class EarlyExit(ABC):
	@abstractmethod
	def __call__(self) -> bool:
		return False


class TextSelection:
	def __init__(self, fulltext: str, position: FullIndex, anchor: FullIndex):
		self.fulltext = fulltext
		self.position = position
		self.anchor = anchor

	def full_index(self, i: SubIndex) -> FullIndex:
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

	def full_size(self) -> int:
		return len(self.fulltext)

	def selection_size(self) -> int:
		return abs(self.position - self.anchor)


class CharacterCase(Enum):
	IGNORE = 0,
	UPPER = 1,
	LOWER = 2,
	CAPITALIZE = 3


class TextIterator:
	def __init__(self, index=SubIndex(0)):
		self.text = TextSelection(AppContext.all_text(), AppContext.text_cursor().position(), AppContext.text_cursor().anchor())
		self.index = index

	def valid(self) -> bool:
		return self.text.is_in_range(self.index)

	def full_index(self) -> FullIndex:
		return self.text.full_index(self.index)

	def char(self) -> str:
		return self.text.char(self.index)

	def is_word_char(self, j: SubIndex | FullIndex | None = None) -> bool:
		return self.text.char(self.index if j is None else j).lower() in SYMBOLS.lowercase_word_characters

	def to_next_char(self) -> None:
		self.index += 1

	def write_char(self, out: StringIO, case: CharacterCase = CharacterCase.IGNORE) -> None:
		match case:
			case CharacterCase.IGNORE:
				out.write(self.char())
			case CharacterCase.UPPER:
				out.write(self.char().upper())
			case CharacterCase.LOWER:
				out.write(self.char().lower())
			case CharacterCase.CAPITALIZE:
				out.write(self.char().upper())
		self.to_next_char()

	def write_chars(self, out: StringIO, num: int, case: CharacterCase = CharacterCase.IGNORE) -> None:
		if case != CharacterCase.CAPITALIZE:
			for _ in range(num):
				self.write_char(out, case)
		else:
			if num > 0:
				self.write_char(out, CharacterCase.UPPER)
			for _ in range(num - 1):
				self.write_char(out, CharacterCase.LOWER)

	# **aBc** => 2
	def left_subword_len(self) -> int:
		if not self.is_word_char():
			return 0

		j = SubIndex(self.index - 1)
		while j >= 0 and self.is_word_char(j):
			j -= 1
		return self.index - j

	def left_subword(self) -> str:
		return self.text.slice(SubIndex(self.index - self.left_subword_len() + 1), self.index)

	# **aBc** => 2
	def right_subword_len(self) -> int:
		if not self.is_word_char():
			return 0

		j = SubIndex(self.index + 1)
		while j < self.text.selection_size() and self.is_word_char(j):
			j += 1
		return j - self.index

	def right_subword(self) -> str:
		return self.text.slice(self.index, SubIndex(self.index + self.right_subword_len()))

	# **aBc** => 2, 5
	def subword_range(self) -> tuple[SubIndex, SubIndex]:
		return SubIndex(self.index - self.left_subword_len() + 1), SubIndex(self.index + self.right_subword_len())

	def subword(self) -> str:
		l, r = self.subword_range()
		return self.text.slice(l, r)

	def is_first_letter_of_subword(self) -> bool:
		return self.is_word_char() and (self.index == 0 or not self.is_word_char(SubIndex(self.index - 1)))

	def distance_to_next_subword(self, early_exit: EarlyExit | None = None) -> int:
		base = self.index
		self.index += self.right_subword_len()
		while self.valid() and not self.is_word_char() and not early_exit():
			self.index += 1
		distance = self.index - base
		self.index = base
		return distance

	def to_next_subword(self, early_exit: EarlyExit | None = None) -> None:
		self.index += self.distance_to_next_subword(early_exit)

	def write_up_to_next_subword(self, out: StringIO, early_exit: EarlyExit | None = None, case: CharacterCase = CharacterCase.IGNORE) -> None:
		d = self.distance_to_next_subword(early_exit)
		while d > 0:
			self.write_char(out, case)
			d -= 1

	# **aBc** => 2
	def left_word_len(self) -> int:
		if not self.is_word_char():
			return 0

		j = FullIndex(self.full_index() - 1)
		while j >= 0 and self.is_word_char(j):
			j -= 1
		return self.full_index() - j

	def left_word(self) -> str:
		return self.text.slice(FullIndex(self.full_index() - self.left_word_len() + 1), self.full_index())

	# **aBc** => 2
	def right_word_len(self) -> int:
		if not self.is_word_char():
			return 0

		j = FullIndex(self.full_index() + 1)
		while j < self.text.full_size() and self.is_word_char(j):
			j += 1
		return j - self.full_index()

	def right_word(self) -> str:
		return self.text.slice(self.full_index(), FullIndex(self.full_index() + self.right_word_len()))

	# **aBc** => 2, 5
	def word_range(self) -> tuple[FullIndex, FullIndex]:
		return FullIndex(self.full_index() - self.left_word_len() + 1), FullIndex(self.full_index() + self.right_word_len())

	def word(self) -> str:
		l, r = self.word_range()
		return self.text.slice(l, r)

	def is_first_letter_of_word(self) -> bool:
		return self.is_word_char() and (self.full_index() == 0 or not self.is_word_char(FullIndex(self.full_index() - 1)))

	def is_first_word_of_sentence(self) -> bool:
		if not self.valid():
			return False

		base = self.index
		self.index -= SubIndex(self.left_word_len())
		prev_word_exists = False
		while self.full_index() >= 0:
			if self.char() in SYMBOLS.sentence_enders:
				break
			elif self.is_word_char():
				prev_word_exists = True
				break
			else:
				self.index -= 1
		self.index = base
		return not prev_word_exists
