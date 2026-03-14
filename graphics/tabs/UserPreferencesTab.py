from dataclasses import dataclass
from typing import override

from graphics import EditorTab, block_signals
from ui import Ui_UserPreferences


@dataclass
class UserPreferences:
	silently_cache_on_close: bool = True


class Strings:
	silently_cache_on_close = "silently_cache_on_close"


STRINGS = Strings()


class UserPreferencesTab(EditorTab):
	def __init__(self):
		self.preferences = UserPreferences()
		self.scratch_preferences = UserPreferences()
		super().__init__("Settings - Preferences", 'user_preferences.toml')

		self.ui = Ui_UserPreferences()
		self.ui.setupUi(self)

		self.ui.onAppCloseBehaviour.currentIndexChanged.connect(self.on_app_close_behaviour_changed)
		self.revert_on_app_close_behaviour = self.revert_button(self.ui.revertOnAppCloseBehaviour, self.strings().silently_cache_on_close)

		self.load()

	@override
	def data(self):
		return self.preferences

	@override
	def scratch_data(self):
		return self.scratch_preferences

	@override
	def revert_buttons(self):
		return [self.revert_on_app_close_behaviour]

	@override
	def strings(self):
		return STRINGS

	@override
	def render_scratch_ui(self, name: str):
		if name == self.strings().silently_cache_on_close:
			with block_signals(self.ui.onAppCloseBehaviour) as el:
				el.setCurrentIndex(0 if self.scratch_data().silently_cache_on_close else 1)

	def on_app_close_behaviour_changed(self, index):
		self.scratch_preferences.silently_cache_on_close = index == 0
		self.revert_on_app_close_behaviour.value_changed()
		self.set_asterisk(True)
