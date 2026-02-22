from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QPlainTextEdit

from processing import Selection


class UndoRedoFilter(QObject):
	def __init__(self, text_edit: QPlainTextEdit, get_cursor, set_cursor):
		super().__init__()
		self.text_edit = text_edit
		self.text_edit.installEventFilter(self)
		self.get_cursor = get_cursor
		self.set_cursor = set_cursor
		self.undo_selections: list[Selection] = [get_cursor()]
		self.redo_selections: list[Selection] = []

		self.can_undo = False

		def on_undo_available(available):
			self.can_undo = available

		self.text_edit.undoAvailable.connect(on_undo_available)

		self.can_redo = False

		def on_redo_available(available):
			self.can_redo = available

		self.text_edit.redoAvailable.connect(on_redo_available)

	def eventFilter(self, watched, event):
		if isinstance(event, QKeyEvent) and event.type() == QEvent.Type.KeyPress and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
			if event.key() == Qt.Key.Key_Z:
				if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
					self.redo()
					return True
				else:
					self.undo()
					return True
			elif event.key() == Qt.Key.Key_Y and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
				self.redo()
				return True

		return super().eventFilter(watched, event)

	def undo(self):
		if self.can_undo:
			self.redo_selections.append(self.get_cursor())
			self.text_edit.undo()
			self.set_cursor(self.undo_selections.pop())

	def redo(self):
		if self.can_redo:
			self.undo_selections.append(self.get_cursor())
			self.text_edit.redo()
			self.set_cursor(self.redo_selections.pop())

	def on_text_operated(self):
		self.redo_selections.clear()
		self.undo_selections.append(self.get_cursor())


class TextArea:
	def __init__(self, text_edit: QPlainTextEdit):
		self.text_edit = text_edit
		self.filter = UndoRedoFilter(self.text_edit, self.selection, self.set_selection)

	def insert_text(self, text):
		self.filter.on_text_operated()
		self.text_edit.insertPlainText(text)

	def append_text(self, text):
		self.filter.on_text_operated()
		self.text_edit.appendPlainText(text)

	def remove_selected_text(self):
		self.filter.on_text_operated()
		self.text_edit.textCursor().removeSelectedText()

	def selection(self) -> Selection:
		cursor = self.text_edit.textCursor()
		return Selection(position=cursor.position(), anchor=cursor.anchor())

	def set_selection(self, selection: Selection):
		cursor = self.text_edit.textCursor()
		cursor.setPosition(selection.anchor)
		cursor.setPosition(selection.position, cursor.MoveMode.KeepAnchor)
		self.text_edit.setTextCursor(cursor)
		self.text_edit.setFocus()

	def all_text(self) -> str:
		return self.text_edit.toPlainText()

	def selected_text(self) -> str:
		return self.text_edit.textCursor().selectedText().replace('\u2029', '\n')
