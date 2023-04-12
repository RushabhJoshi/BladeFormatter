import sublime
import sublime_plugin


class BladeFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, self.view.setting().get("syntax"))
