from typing import override

from processing import TextIterator
from processing.TextIterator import EarlyExit


class EarlyExitAtChar(EarlyExit):
	def __init__(self, it: TextIterator, chars: str):
		self.it = it
		self.chars = chars

	@override
	def __call__(self):
		return self.it.char() in self.chars


class EarlyExitAny(EarlyExit):
	def __init__(self, early_exits: list[EarlyExit]):
		self.early_exits = early_exits

	@override
	def __call__(self):
		return any(early_exit() for early_exit in self.early_exits)


class EarlyExitAll(EarlyExit):
	def __init__(self, early_exits: list[EarlyExit]):
		self.early_exits = early_exits

	@override
	def __call__(self):
		return all(early_exit() for early_exit in self.early_exits)
