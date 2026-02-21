import platform
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMainWindow, QScrollArea

from graphics import FileTab
from storage import PERSISTENT_DATA
from ui import Ui_MainWindow


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		for scroll in self.findChildren(QScrollArea):
			scroll.setFocusPolicy(Qt.FocusPolicy.NoFocus)

		self.ui.fileBasicNew.clicked.connect(self.new_file)
		new_file_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
		new_file_shortcut.activated.connect(self.new_file)
		self.ui.fileBasicOpen.clicked.connect(self.open_file)
		open_file_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
		open_file_shortcut.activated.connect(self.open_file)
		self.ui.fileBasicMove.clicked.connect(self.move_file)
		self.ui.fileBasicDelete.clicked.connect(self.delete_file)
		self.ui.fileBasicSave.clicked.connect(self.save_file)
		save_file_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
		save_file_shortcut.activated.connect(self.save_file)
		self.ui.fileBasicSaveAs.clicked.connect(self.save_file_as)
		self.ui.fileBasicSaveCopy.clicked.connect(self.save_file_copy)
		self.ui.fileBasicSaveAll.clicked.connect(self.save_all_files)
		save_all_files_shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
		save_all_files_shortcut.activated.connect(self.save_all_files)
		self.ui.fileBasicExplorer.clicked.connect(self.open_explorer)

		from processing import get_edit_case_action, EditCaseOption
		self.ui.editCaseUpper.clicked.connect(get_edit_case_action(EditCaseOption.Upper))
		self.ui.editCaseLower.clicked.connect(get_edit_case_action(EditCaseOption.Lower))
		self.ui.editCaseCapitalize.clicked.connect(get_edit_case_action(EditCaseOption.Capitalize))
		self.ui.editCaseSentence.clicked.connect(get_edit_case_action(EditCaseOption.Sentence))
		self.ui.editCaseTitle.clicked.connect(get_edit_case_action(EditCaseOption.Title))

		self.ui.tabWidget.removeTab(0)
		self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

	# TODO(2) ctrl+Z resets text cursor in text area. intercept event in order to create undo action that will restore the text selection while calling QPlainTextEdit undo()/redo().

	def new_file(self):
		self.add_tab(None)

	def open_file(self):
		filenames = PERSISTENT_DATA.get_open_filenames(self)
		for file in filenames:
			self.add_tab(file)

	def add_tab(self, filepath: Path | str | None):
		if isinstance(filepath, str):
			filepath = Path(filepath).resolve()
		tab = FileTab(filepath)
		self.ui.tabWidget.addTab(tab, tab.tabname())
		self.ui.tabWidget.setCurrentWidget(tab)
		tab.on_added()
		tab.focus_text()

	def move_file(self):
		if self.has_tab():
			self.get_tab().move_file()

	def delete_file(self):
		if self.has_tab() and self.get_tab().on_delete():
			self.ui.tabWidget.removeTab(self.ui.tabWidget.currentIndex())

	def save_file(self):
		if self.has_tab():
			self.get_tab().on_save()

	def save_file_as(self):
		if self.has_tab():
			self.get_tab().save_as()

	def save_file_copy(self):
		if self.has_tab():
			self.get_tab().save_copy()

	def save_all_files(self):
		for i in range(self.ui.tabWidget.count()):
			tab = self.get_tab(i)
			tab.on_save()

	def open_explorer(self):
		path = self.get_tab().filepath if self.has_tab() else PERSISTENT_DATA.file_dialog_dir
		if platform.system() == "Windows":
			subprocess.run(["explorer", "/select,", str(path)])
		elif platform.system() == "Darwin":
			subprocess.run(["open", "-R", path])
		else:
			try:
				subprocess.run(["nautilus", "--select", str(path)])
			except FileNotFoundError:
				try:
					subprocess.run(["dolphin", "--select", str(path)])
				except FileNotFoundError:
					subprocess.run(["xdg-open", str(path.parent)])

	def get_tab(self, pos: int | None = None) -> FileTab | None:
		return self.ui.tabWidget.currentWidget() if pos is None else self.ui.tabWidget.widget(pos)

	def has_tab(self):
		return self.ui.tabWidget.count() > 0

	def close_tab(self, pos):  # TODO(1) Close All, Close Others, etc.
		tab = self.get_tab(pos)
		if tab.on_close():  # TODO(1) check on_close() on quitting application
			self.ui.tabWidget.removeTab(pos)
