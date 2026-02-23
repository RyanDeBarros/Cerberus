from abc import ABCMeta, abstractmethod

from PySide6.QtWidgets import QWidget, QMessageBox


class AbstractTabMeta(type(QWidget), ABCMeta):
	pass


class AbstractTab(QWidget, metaclass=AbstractTabMeta):
	def __init__(self):
		super().__init__()
		self.asterisk = False

	def set_asterisk(self, asterisk):
		self.asterisk = asterisk
		self._set_tab_text()

	def _set_tab_text(self):
		import AppContext
		AppContext.main_window().ui.tabWidget.setTabText(self.get_tab_index(), self.tabname())

	def get_tab_index(self):
		import AppContext
		return AppContext.main_window().ui.tabWidget.indexOf(self)

	@abstractmethod
	def raw_tabname(self) -> str:
		pass

	def tabname(self):
		filename = self.raw_tabname()
		return filename if not self.asterisk else f"* {filename}"

	@abstractmethod
	def load(self) -> None:
		pass

	@abstractmethod
	def on_save(self) -> None:
		pass

	def on_close(self):
		if not self.asterisk:
			return True

		mbox = QMessageBox(QMessageBox.Icon.Question, "Unsaved Changes", f"Do you want to save your changes to {self.raw_tabname()}?")
		yes = mbox.addButton("Yes", QMessageBox.ButtonRole.YesRole)
		no = mbox.addButton("No", QMessageBox.ButtonRole.NoRole)
		cancel = mbox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
		mbox.setDefaultButton(cancel)
		mbox.exec()
		if mbox.clickedButton() == yes:
			self.on_save()
		elif mbox.clickedButton() == no:
			pass
		elif mbox.clickedButton() == cancel:
			return False
		return True
