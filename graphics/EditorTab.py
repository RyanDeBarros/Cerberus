from abc import abstractmethod
from typing import override, Callable

from PySide6.QtWidgets import QTabWidget, QPushButton

from graphics import AbstractTab, DynamicStringList, RevertButton
from storage import StorageKeeper, FileSystemLocator


class EditorTab(AbstractTab):
	def __init__(self, name: str, settings_filename: str):
		super().__init__()
		self.name = name
		self.opened = False

		self.string_attrs: list[str] = [name for name, _ in self.strings().__class__.__dict__.items() if not name.startswith("__")]
		self.storage = StorageKeeper(self.data(), self.string_attr_vars(), FileSystemLocator.SETTINGS_PATH / settings_filename, FileSystemLocator.DEFAULTS_PATH / settings_filename)

	@override
	def raw_tabname(self) -> str:
		return self.name

	@override
	def on_save(self):
		if self.asterisk:
			self.dump()
			self.set_asterisk(False)

	@override
	def load(self):
		self.storage.load()
		self.storage.dump_to(self.scratch_data())
		self.render_all_scratch_ui()  # TODO(1) also call value_changed() on all revert buttons

	def dump(self):
		self.storage.load_from(self.scratch_data())
		self.storage.dump()

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

	@override
	def on_app_close(self):
		self.close()

	@abstractmethod
	def data(self):
		raise NotImplementedError()

	@abstractmethod
	def scratch_data(self):
		raise NotImplementedError()

	@abstractmethod
	def strings(self):
		raise NotImplementedError()

	def string_attr_vars(self):
		return [getattr(self.strings(), attr) for attr in self.string_attrs]

	def revert_button(self, btn: QPushButton, name: str):
		return RevertButton(btn, self.storage.get_default_attr(name), self.revert_getter(name), self.revert_setter(name))

	def revert_getter(self, name: str):
		def f():
			return getattr(self.scratch_data(), name)
		return f

	def revert_setter(self, name: str):
		def f(value):
			if getattr(self.scratch_data(), name) != value:
				setattr(self.scratch_data(), name, value)
				self.set_asterisk(self.data() != self.scratch_data())
				self.render_scratch_ui(name)
		return f

	def render_all_scratch_ui(self):
		for key in self.string_attrs:
			self.render_scratch_ui(key)

	@abstractmethod
	def render_scratch_ui(self, name: str):
		pass

	def open_strings_list_dialog(self, name: str, reverter: RevertButton, op: Callable[[list[str]], None] | None = None):
		new_strings, modified = DynamicStringList.dialog(getattr(self.scratch_data(), name))
		if not modified:
			return

		if op is not None:
			op(new_strings)

		setattr(self.scratch_data(), name, new_strings)
		reverter.value_changed()
		if new_strings != getattr(self.data(), name):
			self.set_asterisk(True)

	def open_strings_set_dialog(self, name: str, reverter: RevertButton, op: Callable[[list[str]], None] | None = None):
		new_strings, modified = DynamicStringList.dialog(sorted(getattr(self.scratch_data(), name)))
		if not modified:
			return

		if op is not None:
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
