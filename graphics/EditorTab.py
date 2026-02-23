from abc import abstractmethod
from typing import override

from PySide6.QtWidgets import QTabWidget

from graphics import AbstractTab, DynamicStringList
from storage import StorageKeeper


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

	# def rvt_get_temp_value(self, obj, name: str):
	# 	def f():
	# 		if name in self.temp:
	# 			return self.temp[name]
	# 		else:
	# 			return getattr(obj, name)
	# 	return f
	#
	# def rvt_set_temp_value(self, name: str):
	# 	def f(value):
	# 		self.temp[name] = value
	# 	return f
	#
	# @staticmethod
	# def rvt_get_default_value(storage: StorageKeeper, name: str):
	# 	def f():
	# 		return storage.get_default_attr(name)
	# 	return f
