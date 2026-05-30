import sublime
import sublime_plugin
import subprocess
import os

class BladeFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 1. Quick sanity check: Is this actually a blade file?
        filename = self.view.file_name() or ""
        if not filename.endswith(".blade.php") and "blade" not in self.view.settings().get('syntax').lower():
            # Feel free to change this if you want it to run on any unsaved file
            sublime.status_message("Blade Formatter: Not a Blade file.")
            return

        # 2. Capture the entire file contents
        entire_region = sublime.Region(0, self.view.size())
        unformatted_code = self.view.substr(entire_region)

        if not unformatted_code.strip():
            return

        # 3. Save the editor's current viewport scroll position
        current_viewport = self.view.viewport_position()

        # 4. Set up the terminal execution command
        # On Windows, 'shell=True' is often needed to locate global npm binaries
        cmd = ["blade-formatter", "--stdin"]

        # Load user settings and append CLI flags
        settings = sublime.load_settings("BladeFormatter.sublime-settings")

        # 1. indent_size
        indent_size = settings.get("indent_size")
        if indent_size is not None:
            cmd.extend(["--indent-size", str(indent_size)])

        # 2. wrap_attributes
        wrap_attributes = settings.get("wrap_attributes")
        if wrap_attributes:
            cmd.extend(["--wrap-attributes", str(wrap_attributes)])

        # 3. wrap_line_length
        wrap_line_length = settings.get("wrap_line_length")
        if wrap_line_length is not None:
            cmd.extend(["--wrap-line-length", str(wrap_line_length)])

        # 4. wrap_attributes_min_attrs
        wrap_attributes_min_attrs = settings.get("wrap_attributes_min_attrs")
        if wrap_attributes_min_attrs is not None:
            cmd.extend(["--wrap-attributes-min-attrs", str(wrap_attributes_min_attrs)])

        # 5. indent_inner_html
        if settings.get("indent_inner_html", False):
            cmd.append("--indent-inner-html")

        # 6. end_with_newline
        if settings.get("end_with_newline", True) is False:
            cmd.append("--no-end-with-newline")

        # 7. end_of_line
        end_of_line = settings.get("end_of_line")
        if end_of_line:
            cmd.extend(["--end-of-line", str(end_of_line)])

        # 8. use_tabs
        if settings.get("use_tabs", False):
            cmd.append("--use-tabs")

        # 9. sort_tailwindcss_classes
        if settings.get("sort_tailwindcss_classes", False):
            cmd.append("--sort-tailwindcss-classes")

        # 10. tailwindcss_config_path
        tailwindcss_config_path = settings.get("tailwindcss_config_path")
        if tailwindcss_config_path:
            cmd.extend(["--tailwindcss-config-path", str(tailwindcss_config_path)])

        # 11. sort_html_attributes
        sort_html_attributes = settings.get("sort_html_attributes")
        if sort_html_attributes and sort_html_attributes != "none":
            cmd.extend(["--sort-html-attributes", str(sort_html_attributes)])

        # 12. no_multiple_empty_lines
        if settings.get("no_multiple_empty_lines", False):
            cmd.append("--no-multiple-empty-lines")

        # 13. no_php_syntax_check
        if settings.get("no_php_syntax_check", False):
            cmd.append("--no-php-syntax-check")

        # 14. no_single_quote
        if settings.get("no_single_quote", False):
            cmd.append("--no-single-quote")

        # 15. no_trailing_comma_php
        if settings.get("no_trailing_comma_php", False):
            cmd.append("--no-trailing-comma-php")

        # 16. extra_liners
        extra_liners = settings.get("extra_liners")
        if extra_liners:
            if isinstance(extra_liners, list):
                extra_liners_str = ",".join(str(x) for x in extra_liners)
            else:
                extra_liners_str = str(extra_liners)
            if extra_liners_str:
                cmd.extend(["--extra-liners", extra_liners_str])

        # 17. component_prefix
        component_prefix = settings.get("component_prefix")
        if component_prefix:
            if isinstance(component_prefix, list):
                component_prefix_str = ",".join(str(x) for x in component_prefix)
            else:
                component_prefix_str = str(component_prefix)
            if component_prefix_str:
                cmd.extend(["--component-prefix", component_prefix_str])

        # 18. php_version
        php_version = settings.get("php_version")
        if php_version:
            cmd.extend(["--php-version", str(php_version)])

        is_windows = os.name == 'nt'

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=is_windows
            )
            
            stdout_bytes, stderr_bytes = process.communicate(input=unformatted_code.encode('utf-8'))
            formatted_code = stdout_bytes.decode('utf-8').replace('\r', '') if stdout_bytes else ""
            stderr = stderr_bytes.decode('utf-8').replace('\r', '') if stderr_bytes else ""

            # 5. Check if the external tool threw an error
            if process.returncode != 0:
                print("Blade Formatter Error:\n", stderr)
                sublime.error_message("Blade Formatter Error! Check the Sublime console for details.")
                return

            # 6. Replace the old code with the beautiful new code
            if formatted_code and formatted_code != unformatted_code:
                self.view.replace(edit, entire_region, formatted_code)
                sublime.status_message("Blade file formatted successfully!")
            
            # 7. Restore the user's scroll position so they don't lose their spot
            # Sublime needs a tiny delay to compute the layout change
            sublime.set_timeout(lambda: self.view.set_viewport_position(current_viewport, False), 50)

        except FileNotFoundError:
            sublime.error_message("Could not find 'blade-formatter'. Make sure it is installed globally via npm (npm i -g blade-formatter).")