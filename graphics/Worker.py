from PySide6.QtCore import QObject, QTimer, Slot


class Worker(QObject):
	def __init__(self, func, interval_ms):
		super().__init__()
		self.func = func
		self.timer = QTimer(self)
		self.timer.setInterval(interval_ms)
		self.timer.timeout.connect(self.run)

	@Slot()
	def start(self):
		self.timer.start()

	@Slot()
	def stop(self):
		self.timer.stop()

	@Slot()
	def run(self):
		self.func()
