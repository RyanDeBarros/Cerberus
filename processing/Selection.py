from contextlib import contextmanager


class Selection:
	position: int = 0
	anchor: int = 0


@contextmanager
def restore_selection():
	import AppContext
	sel = AppContext.text_area().selection()
	yield sel
	AppContext.text_area().set_selection(sel)
