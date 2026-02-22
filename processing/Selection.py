from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Selection:
	position: int = 0
	anchor: int = 0


@contextmanager
def restore_selection():
	from graphics import AppContext
	sel = AppContext.text_area().selection()
	yield sel
	AppContext.text_area().set_selection(sel)
