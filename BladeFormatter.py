import sublime
import sublime_plugin
import os


class BladeFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()
		command = "blade-formatter --write " + file_name
		if self.view.file_name().endswith('.blade.php'):
			os.system(command)
