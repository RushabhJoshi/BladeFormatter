import sublime
import sublime_plugin
import os


class BladeFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()
		command = "blade-formatter --write " + file_name
		if self.view.file_name().endswith('.blade.php'):
			os.system(command)

class MySaveListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        if view.file_name().endswith('.blade.php'):
            view.run_command('blade_formatter')
