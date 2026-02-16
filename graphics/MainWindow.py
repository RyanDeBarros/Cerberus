import os.path
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMainWindow, QScrollArea, QFileDialog

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

		from processing import get_edit_case_action, EditCaseOption
		self.ui.editCaseUpper.clicked.connect(get_edit_case_action(EditCaseOption.Upper))
		self.ui.editCaseLower.clicked.connect(get_edit_case_action(EditCaseOption.Lower))
		self.ui.editCaseCapitalize.clicked.connect(get_edit_case_action(EditCaseOption.Capitalize))
		self.ui.editCaseSentence.clicked.connect(get_edit_case_action(EditCaseOption.Sentence))
		self.ui.editCaseTitle.clicked.connect(get_edit_case_action(EditCaseOption.Title))

		self.ui.tabWidget.removeTab(0)
		self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
		# TODO ctrl+Z resets text cursor in text area. intercept event in order to create undo action that will restore the text selection while calling QPlainTextEdit undo()/redo().

	def new_file(self):
		self.ui.tabWidget.addTab(FileTab("Untitled"), "Untitled")

	def open_file(self):
		filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", PERSISTENT_DATA.file_dialog_dir, "Text Files (*.txt *.md *.log);; All Files (*)")
		if filenames:
			PERSISTENT_DATA.file_dialog_dir = os.path.dirname(filenames[0])
			PERSISTENT_DATA.store()
			for file in filenames:
				self.open_file_content(file)

	def open_file_content(self, file):
		self.get_tab().text_area.setPlainText(Path(file).read_text())  # TODO don't open if file is too big - set maximum in settings

	def move_file(self):
		pass  # TODO

	def delete_file(self):
		pass  # TODO make sure to prompt for confirmation first

	def save_file(self):
		pass  # TODO

	def save_file_as(self):
		pass  # TODO

	def save_file_copy(self):
		pass  # TODO

	def save_all_files(self):
		pass  # TODO

	def get_tab(self, pos: int | None = None) -> FileTab:
		return self.ui.tabWidget.currentWidget() if pos is None else self.ui.tabWidget.widget(pos)

	def close_tab(self, pos):
		self.ui.tabWidget.removeTab(pos)  # TODO confirmation if unsaved changes
