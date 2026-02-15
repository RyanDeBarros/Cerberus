import os.path
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMainWindow, QScrollArea, QFileDialog

from storage import PERSISTENT_DATA
from ui import Ui_MainWindow


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.textArea.setFocus()

		for scroll in self.findChildren(QScrollArea):
			scroll.setFocusPolicy(Qt.FocusPolicy.NoFocus)

		from processing import get_edit_case_action, EditCaseOption
		self.ui.editCaseUpper.clicked.connect(get_edit_case_action(EditCaseOption.Upper))
		self.ui.editCaseLower.clicked.connect(get_edit_case_action(EditCaseOption.Lower))
		self.ui.editCaseCapitalize.clicked.connect(get_edit_case_action(EditCaseOption.Capitalize))
		self.ui.editCaseSentence.clicked.connect(get_edit_case_action(EditCaseOption.Sentence))
		self.ui.editCaseTitle.clicked.connect(get_edit_case_action(EditCaseOption.Title))

		open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
		open_shortcut.activated.connect(self.open_file_prompt)
		# TODO ctrl+Z is removes focus from text area

	def open_file_prompt(self):
		filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", PERSISTENT_DATA.file_dialog_dir, "Text Files (*.txt *.md *.log);; All Files (*)")
		if filenames:
			PERSISTENT_DATA.file_dialog_dir = os.path.dirname(filenames[0])
			PERSISTENT_DATA.store()
			for file in filenames:
				self.open_file(file)

	def open_file(self, file):
		self.ui.textArea.setPlainText(Path(file).read_text())
