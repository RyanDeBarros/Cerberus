from PySide6.QtWidgets import QPushButton


class RevertButton:
	def __init__(self, btn: QPushButton, get_value, set_value, get_default):
		self.btn = btn
		self.btn.setText("\u27F2")
		self.btn.clicked.connect(self.on_clicked)
		self.get_value = get_value
		self.set_value = set_value
		self.get_default = get_default
		self.value_changed()

	def value_changed(self):
		if self.get_value() == self.get_default():
			self.btn.hide()
		else:
			self.btn.show()

	def on_clicked(self):
		self.set_value(self.get_default())
		self.btn.hide()
