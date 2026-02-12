from PySide6.QtWidgets import QPushButton


class ToolButton:
	def __init__(self, button: QPushButton, action: callable):
		self.button = button
		self.button.clicked.connect(action)
