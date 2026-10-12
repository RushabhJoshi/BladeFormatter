# pyrefly: ignore [missing-import]
import sublime
# pyrefly: ignore [missing-import]
import sublime_plugin
import os
import shutil
import subprocess

_running_views = set()


class BladeFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 1. Quick sanity check: Is this actually a blade file?
        filename = self.view.file_name() or ""
        syntax = self.view.settings().get('syntax') or ""
        if not filename.endswith(".blade.php") and "blade" not in syntax.lower():
            sublime.status_message("Blade Formatter: Not a Blade file.")
            return

        # 2. Capture the entire file contents
        entire_region = sublime.Region(0, self.view.size())
        unformatted_code = self.view.substr(entire_region)

        if not unformatted_code.strip():
            return

        view_id = self.view.id()
        if view_id in _running_views:
            sublime.status_message("Blade Formatter: Format already in progress.")
            return

        # 3. Save the editor's current viewport scroll position
        current_viewport = self.view.viewport_position()

        cmd = self._build_command()
        resolved = shutil.which(cmd[0])
        if resolved:
            cmd[0] = resolved

        _running_views.add(view_id)
        sublime.status_message("Blade Formatter: Formatting...")
        sublime.set_timeout_async(
            lambda: self._run_formatter(cmd, unformatted_code, current_viewport, view_id),
            0
        )

    def _build_command(self):
        cmd = ["blade-formatter", "--stdin"]
        settings = sublime.load_settings("BladeFormatter.sublime-settings")

        indent_size = settings.get("indent_size")
        if indent_size is not None:
            cmd.extend(["--indent-size", str(indent_size)])

        wrap_attributes = settings.get("wrap_attributes")
        if wrap_attributes:
            cmd.extend(["--wrap-attributes", str(wrap_attributes)])

        wrap_line_length = settings.get("wrap_line_length")
        if wrap_line_length is not None:
            cmd.extend(["--wrap-line-length", str(wrap_line_length)])

        wrap_attributes_min_attrs = settings.get("wrap_attributes_min_attrs")
        if wrap_attributes_min_attrs is not None:
            cmd.extend(["--wrap-attributes-min-attrs", str(wrap_attributes_min_attrs)])

        if settings.get("indent_inner_html", False):
            cmd.append("--indent-inner-html")

        if settings.get("end_with_newline", True) is False:
            cmd.append("--no-end-with-newline")

        end_of_line = settings.get("end_of_line")
        if end_of_line:
            cmd.extend(["--end-of-line", str(end_of_line)])

        if settings.get("use_tabs", False):
            cmd.append("--use-tabs")

        if settings.get("sort_tailwindcss_classes", False):
            cmd.append("--sort-tailwindcss-classes")

        tailwindcss_config_path = settings.get("tailwindcss_config_path")
        if tailwindcss_config_path:
            cmd.extend(["--tailwindcss-config-path", str(tailwindcss_config_path)])

        sort_html_attributes = settings.get("sort_html_attributes")
        if sort_html_attributes and sort_html_attributes != "none":
            cmd.extend(["--sort-html-attributes", str(sort_html_attributes)])

        if settings.get("no_multiple_empty_lines", False):
            cmd.append("--no-multiple-empty-lines")

        if settings.get("no_php_syntax_check", False):
            cmd.append("--no-php-syntax-check")

        if settings.get("no_single_quote", False):
            cmd.append("--no-single-quote")

        if settings.get("no_trailing_comma_php", False):
            cmd.append("--no-trailing-comma-php")

        extra_liners = settings.get("extra_liners")
        if extra_liners:
            if isinstance(extra_liners, list):
                extra_liners_str = ",".join(str(x) for x in extra_liners)
            else:
                extra_liners_str = str(extra_liners)
            if extra_liners_str:
                cmd.extend(["--extra-liners", extra_liners_str])

        component_prefix = settings.get("component_prefix")
        if component_prefix:
            if isinstance(component_prefix, list):
                component_prefix_str = ",".join(str(x) for x in component_prefix)
            else:
                component_prefix_str = str(component_prefix)
            if component_prefix_str:
                cmd.extend(["--component-prefix", component_prefix_str])

        php_version = settings.get("php_version")
        if php_version:
            cmd.extend(["--php-version", str(php_version)])

        return cmd

    def _run_formatter(self, cmd, unformatted_code, current_viewport, view_id):
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo
            )
            stdout_bytes, stderr_bytes = process.communicate(
                input=unformatted_code.encode('utf-8')
            )
            formatted_code = stdout_bytes.decode('utf-8').replace('\r', '') if stdout_bytes else ""
            stderr = stderr_bytes.decode('utf-8').replace('\r', '') if stderr_bytes else ""

            if process.returncode != 0:
                self._notify_error(
                    "[BladeFormatter] Blade Formatter Error:\n{}".format(stderr),
                    "Blade Formatter Error! Check the Sublime console for details."
                )
                return

            sublime.set_timeout(
                lambda: self._apply_result(formatted_code, unformatted_code, current_viewport),
                0
            )
        except FileNotFoundError:
            self._notify_error(
                "[BladeFormatter] Error: blade-formatter executable not found in PATH.",
                "Could not find 'blade-formatter'. Make sure it is installed globally via npm (npm i -g blade-formatter)."
            )
        except Exception as e:
            self._notify_error(
                "[BladeFormatter] Unexpected error: {}".format(str(e)),
                "Blade Formatter Unexpected Error: " + str(e)
            )
        finally:
            _running_views.discard(view_id)

    def _apply_result(self, formatted_code, unformatted_code, current_viewport):
        if not self.view.is_valid():
            return

        current_code = self.view.substr(sublime.Region(0, self.view.size()))
        if current_code != unformatted_code:
            sublime.status_message("Blade Formatter: Buffer changed; skipped applying format.")
            return

        if formatted_code and formatted_code != unformatted_code:
            self.view.run_command("blade_format_replace", {"formatted_code": formatted_code})
            sublime.status_message("Blade file formatted successfully!")
        else:
            sublime.status_message("Blade Formatter: Already formatted.")

        sublime.set_timeout(lambda: self.view.set_viewport_position(current_viewport, False), 50)

    def _notify_error(self, console_msg, dialog_msg):
        def show():
            print(console_msg)
            sublime.error_message(dialog_msg)

        sublime.set_timeout(show, 0)


class BladeFormatReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, formatted_code):
        entire_region = sublime.Region(0, self.view.size())
        self.view.replace(edit, entire_region, formatted_code)
