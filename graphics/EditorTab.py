from abc import abstractmethod
from typing import override, Callable

from PySide6.QtWidgets import QTabWidget, QPushButton

from graphics import AbstractTab, DynamicStringList, RevertButton
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
			self.dump()
			self.set_asterisk(False)

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

	@abstractmethod
	def storage_keeper(self) -> StorageKeeper:
		pass

	@abstractmethod
	def data(self):
		pass

	@abstractmethod
	def scratch_data(self):
		pass

	def revert_button(self, btn: QPushButton, name: str):
		return RevertButton(btn, self.storage_keeper().get_default_attr(name), self.revert_getter(name), self.revert_setter(name))

	def revert_getter(self, name: str):
		def f():
			return getattr(self.scratch_data(), name)
		return f

	def revert_setter(self, name: str):
		def f(value):
			if getattr(self.scratch_data(), name) != value:
				setattr(self.scratch_data(), name, value)
				self.set_asterisk(True)
		return f

	def open_strings_list_dialog(self, name: str, reverter: RevertButton, op: Callable[[list[str]], None] | None = None):
		new_strings, modified = DynamicStringList.dialog(getattr(self.scratch_data(), name))
		if not modified:
			return

		if op:
			op(new_strings)

		setattr(self.scratch_data(), name, new_strings)
		reverter.value_changed()
		if new_strings != getattr(self.data(), name):
			self.set_asterisk(True)

	def open_strings_set_dialog(self, name: str, reverter: RevertButton, op: Callable[[list[str]], None] | None = None):
		new_strings, modified = DynamicStringList.dialog(sorted(getattr(self.scratch_data(), name)))
		if not modified:
			return

		if op:
			op(new_strings)
		new_strings = set(new_strings)

		setattr(self.scratch_data(), name, new_strings)
		reverter.value_changed()
		if new_strings != getattr(self.data(), name):
			self.set_asterisk(True)

	@staticmethod
	def strings_list_to_lower_op(strings: list[str]):
		for i in range(len(strings)):
			strings[i] = strings[i].lower()
