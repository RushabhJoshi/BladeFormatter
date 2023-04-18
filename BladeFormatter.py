import sublime
import sublime_plugin
import subprocess
from sublime import load_settings

# def convert_to_args()

class BladeFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		whole_region = sublime.Region(0, self.view.size())
		text = self.view.substr(whole_region)
		settings = load_settings("BladeFormatter.sublime-settings")
		command = ["blade-formatter"]
		args = [
			"--indent-size", str(settings.get("indent_size")),
			"--wrap-attributes", str(settings.get("wrap_attributes")),
			"--wrap-line-length", str(settings.get("wrap_line_length")),
			"--end-with-newline", str(settings.get("end_with_newline")),
			"--end-of-line", str(settings.get("end_of_line")),
			"--sort-tailwindcss-classes", str(settings.get("sort_tailwindcss_classes")),
			"--sort-html-attributes", str(settings.get("sort_html_attributes")),
			"--no-multiple-empty-lines", str(settings.get("no_multiple_empty_lines")),
			"--no-php-syntax-check", str(settings.get("no_php_syntax_check")),
		]
		stdin = ["--stdin"]
		command = command + args + stdin
		if self.view.file_name().endswith('.blade.php'):
			stdout, stderr = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(input=text.encode())
			self.view.replace(edit, whole_region, stdout.decode())

class BladeFormatterListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.file_name().endswith('.blade.php'):
            view.run_command('blade_formatter')
