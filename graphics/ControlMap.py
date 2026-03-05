from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QAbstractSlider

from graphics import TextArea


class ControlMap(QObject):
	def __init__(self, text_area: TextArea):
		super().__init__()
		self.text_area = text_area
		self.text_area.text_edit.installEventFilter(self)

	def eventFilter(self, watched, event):
		if event.type() == QEvent.Type.KeyPress and isinstance(event, QKeyEvent):
			if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
				if self.scroll(event):
					return True
		return super().eventFilter(watched, event)

	def scroll(self, event: QKeyEvent):
		scrollbar = self.text_area.text_edit.verticalScrollBar()
		if event.key() == Qt.Key.Key_Up:
			scrollbar.triggerAction(QAbstractSlider.SliderAction.SliderSingleStepSub)
		elif event.key() == Qt.Key.Key_Down:
			scrollbar.triggerAction(QAbstractSlider.SliderAction.SliderSingleStepAdd)
		else:
			return False
		return True

# TODO(3) Other key shortcuts for duplicate line, select line/word, delete line, etc. (like IDEs + vim controls)
