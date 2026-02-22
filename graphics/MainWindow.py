import platform
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMainWindow, QScrollArea, QMenu

from graphics import FileTab, AbstractTab
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
		self.ui.fileBasicReload.clicked.connect(self.reload_file)
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

		self.ui.tabWidget.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
		self.ui.tabWidget.tabBar().customContextMenuRequested.connect(self.on_tab_context_menu)

		self.ui.tabWidget.removeTab(0)
		self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

	# TODO(2) upon quitting application, cache the tabs that are currently open and their buffers (don't check on_close(), just cache unsaved edits for when the app is re-opened). Probable edges cases with cache when multiple instances of Cerberus are running.

	def on_tab_context_menu(self, pos):
		index = self.ui.tabWidget.tabBar().tabAt(pos)
		if index == -1:
			return

		menu = QMenu(self)
		close_action = menu.addAction("Close")
		close_all_action = menu.addAction("Close All")
		close_others_action = menu.addAction("Close Others")
		action = menu.exec(self.ui.tabWidget.tabBar().mapToGlobal(pos))

		if action == close_action:
			self.close_tab(index)
		elif action == close_all_action:
			for _ in range(self.ui.tabWidget.count()):
				self.close_tab(0)
		elif action == close_others_action:
			after = self.ui.tabWidget.count() - 1 - index
			if after > 0:
				for _ in range(after):
					self.close_tab(self.ui.tabWidget.count() - 1)
			if index > 0:
				for _ in range(index):
					self.close_tab(0)

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
		if self.on_file_tab():
			self.get_file_tab().move_file()

	def reload_file(self):
		if self.on_file_tab():
			self.get_file_tab().load()

	def delete_file(self):
		if self.on_file_tab() and self.get_file_tab().on_delete():
			self.ui.tabWidget.removeTab(self.ui.tabWidget.currentIndex())

	def save_file(self):
		if self.on_file_tab():
			self.get_file_tab().on_save()

	def save_file_as(self):
		if self.on_file_tab():
			self.get_file_tab().save_as()

	def save_file_copy(self):
		if self.on_file_tab():
			self.get_file_tab().save_copy()

	def save_all_files(self):
		for i in range(self.ui.tabWidget.count()):
			self.get_tab(i).on_save()

	def open_explorer(self):
		if not self.on_file_tab():
			return

		path = self.get_file_tab().filepath if self.on_file_tab() else PERSISTENT_DATA.file_dialog_dir
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

	def has_tab(self):
		return self.ui.tabWidget.count() > 0

	def get_tab(self, pos: int | None) -> AbstractTab:
		return self.ui.tabWidget.widget(pos) if pos else self.ui.tabWidget.currentWidget()

	def on_file_tab(self) -> bool:
		return self.has_tab() and isinstance(self.ui.tabWidget.currentWidget(), FileTab)

	def get_file_tab(self) -> FileTab:
		return self.ui.tabWidget.currentWidget()

	def close_tab(self, pos):
		if self.get_tab(pos).on_close():
			self.ui.tabWidget.removeTab(pos)
