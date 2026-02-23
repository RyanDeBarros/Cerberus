from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QWidget, QListView, QDialog, QVBoxLayout

from ui import Ui_DynamicList


class DynamicStringList(QWidget):
	def __init__(self, items: list[str]):
		super().__init__()
		self.ui = Ui_DynamicList()
		self.ui.setupUi(self)

		self.model = QStringListModel(items)
		self.ui.listView.setModel(self.model)

		self.ui.btnNew.clicked.connect(self.new_item)
		self.ui.btnDelete.clicked.connect(self.delete_item)

		self.untouched = True

	def new_item(self):
		items = self.model.stringList()
		items.append("New Item")
		self.model.setStringList(items)
		self.untouched = False

	def delete_item(self):
		indexes = self.ui.listView.selectedIndexes()
		if not indexes:
			return

		items = self.model.stringList()
		for index in sorted(indexes, reverse=True):
			items.pop(index.row())
		self.model.setStringList(items)
		self.untouched = False

	def get_items(self):
		return self.model.stringList()

	@staticmethod
	def dialog(items: list[str]):
		dlg = QDialog()
		layout = QVBoxLayout(dlg)
		strings = DynamicStringList(items)
		layout.addWidget(strings)
		dlg.exec()

		new_items = strings.get_items()
		print(new_items)
