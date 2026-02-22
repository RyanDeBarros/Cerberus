from contextlib import contextmanager
from dataclasses import dataclass

from graphics import AppContext


@dataclass
class Selection:
	position: int = 0
	anchor: int = 0

	@staticmethod
	def from_cursor():
		cursor = AppContext.text_cursor()
		return Selection(position=cursor.position(), anchor=cursor.anchor())

	def send_to_cursor(self):
		cursor = AppContext.text_cursor()
		cursor.setPosition(self.anchor)
		cursor.setPosition(self.position, cursor.MoveMode.KeepAnchor)
		AppContext.set_text_cursor(cursor)


@contextmanager
def restore_selection():
	sel = Selection.from_cursor()
	yield sel
	sel.send_to_cursor()
