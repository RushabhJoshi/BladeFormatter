import sublime
import sublime_plugin
import subprocess


class BladeFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		whole_region = sublime.Region(0, self.view.size())
		text = self.view.substr(whole_region)
		command = ["blade-formatter", "--stdin"]
		if self.view.file_name().endswith('.blade.php'):
			stdout, stderr = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(input=text.encode())
			self.view.replace(edit, whole_region, stdout.decode())

class BladeFormatterListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.file_name().endswith('.blade.php'):
            view.run_command('blade_formatter')
