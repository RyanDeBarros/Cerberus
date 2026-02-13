from PySide6.QtWidgets import QPushButton


class ToolButton:
	def __init__(self, button: QPushButton, action: callable):
		self.button = button
		self.button.clicked.connect(action)
		# TODO button should not steal focus from text area - or any other ui element for that matter
