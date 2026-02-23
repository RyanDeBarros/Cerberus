from PySide6.QtWidgets import QPushButton


class RevertButton:
	def __init__(self, btn: QPushButton, default_value, getter, setter):
		self.btn = btn
		self.btn.setText("\u27F2")
		self.btn.clicked.connect(self.on_clicked)
		self.default_value = default_value
		self.getter = getter
		self.setter = setter
		self.value_changed()

	def value_changed(self):
		if self.getter() == self.default_value:
			self.btn.hide()
		else:
			self.btn.show()

	def on_clicked(self):
		self.setter(self.default_value)
		self.btn.hide()
