from dataclasses import dataclass
from typing import override

from graphics import EditorTab, block_signals
from storage import StorageKeeper, FileSystemLocator
from ui import Ui_UserPreferences


@dataclass
class UserPreferences:
	silently_cache_on_close: bool = True


class Strings:
	silently_cache_on_close = "silently_cache_on_close"

STRINGS = Strings()

STRINGS_ATTRS: list[str] = [name for name, _ in STRINGS.__class__.__dict__.items() if not name.startswith("__")]


class UserPreferencesTab(EditorTab):
	def __init__(self):
		super().__init__("Settings - Symbols")
		self.preferences = UserPreferences()
		self.scratch_preferences = UserPreferences()
		self.storage = StorageKeeper(self.preferences, [
			STRINGS.silently_cache_on_close,
		], FileSystemLocator.SETTINGS_PATH / 'user_preferences.toml', FileSystemLocator.DEFAULTS_PATH / 'user_preferences.toml')

		self.ui = Ui_UserPreferences()
		self.ui.setupUi(self)

		self.ui.onAppCloseBehaviour.currentIndexChanged.connect(self.on_app_close_behaviour_changed)
		self.revert_on_app_close_behaviour = self.revert_button(self.ui.revertOnAppCloseBehaviour, STRINGS.silently_cache_on_close)

		self.load()

	@override
	def storage_keeper(self) -> StorageKeeper:
		return self.storage

	@override
	def data(self):
		return self.preferences

	@override
	def scratch_data(self):
		return self.scratch_preferences

	def on_app_close_behaviour_changed(self, index):
		self.scratch_preferences.silently_cache_on_close = index == 0
		self.revert_on_app_close_behaviour.value_changed()
		self.set_asterisk(True)

	@override
	def render_all_scratch_ui(self):
		for key in STRINGS_ATTRS:  # TODO(1) make render_all_scratch_ui() non-abstract and make strings() an abstract method in EditorTab
			self.render_scratch_ui(key)

	@override
	def render_scratch_ui(self, name: str):
		match name:
			case STRINGS.silently_cache_on_close:
				with block_signals(self.ui.onAppCloseBehaviour) as el:
					el.setCurrentIndex(0 if self.scratch_data().silently_cache_on_close else 1)
