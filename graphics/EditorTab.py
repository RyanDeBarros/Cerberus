from abc import abstractmethod
from typing import override

from PySide6.QtWidgets import QTabWidget

from graphics import AbstractTab


class EditorTab(AbstractTab):
	def __init__(self, name: str):
		super().__init__()
		self.name = name
		self.opened = False

	@override
	def raw_tabname(self) -> str:
		return self.name

	@override
	def on_save(self):
		if self.asterisk:
			self.set_asterisk(False)
			self.dump()

	@abstractmethod
	def dump(self):
		pass

	def open(self, holder: QTabWidget):
		if not self.opened:
			self.opened = True
			holder.addTab(self, self.tabname())
			self.load()

		holder.setCurrentWidget(self)

	@override
	def on_close(self):
		if super().on_close():
			self.opened = False
			return True
		else:
			return False
