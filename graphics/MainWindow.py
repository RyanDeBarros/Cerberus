from PySide6.QtWidgets import QMainWindow

from ui import Ui_MainWindow


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		from graphics import ToolButton

		from graphics import get_edit_case_action, EditCaseOption
		self.editCaseUpper = ToolButton(self.ui.editCaseUpper, get_edit_case_action(EditCaseOption.Upper))
		self.editCaseLower = ToolButton(self.ui.editCaseLower, get_edit_case_action(EditCaseOption.Lower))
		self.editCaseCapitalize = ToolButton(self.ui.editCaseCapitalize, get_edit_case_action(EditCaseOption.Capitalize))
		self.editCaseSentence = ToolButton(self.ui.editCaseSentence, get_edit_case_action(EditCaseOption.Sentence))
		self.editCaseTitle = ToolButton(self.ui.editCaseTitle, get_edit_case_action(EditCaseOption.Title))
