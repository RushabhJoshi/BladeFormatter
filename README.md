Blade Formatter
===============

Blade Formatter is a Sublime Text package that helps you to format your Laravel Blade templates as per PSR standards.

Requirements
------------
To use this package you need to install node package globaly [blade-formatter](https://github.com/shufo/blade-formatter).

Installation
------------

To install Blade Formatter, you can use Sublime Text's Package Control. Follow these steps:

1.  Open the command palette by pressing `Ctrl+Shift+P` on Windows or `Cmd+Shift+P` on Mac
2.  Type `Package Control: Install Package` and press `Enter`
3.  Search for `Blade Formatter` and press `Enter` to install

Alternatively, you can install it manually by cloning this repository to your Sublime Text's Packages directory.

Usage
-----

You can format your Blade templates by using the `Format: Blade File` command. Here's how to do it:

1.  Open a Blade template file
2.  Press `Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on Mac to open the command palette
3.  Type `Format: Blade File` and press `Enter`

Alternatively, you can use the keyboard shortcut `Shift+Alt+F` (`Shift+Option+F` on Mac) to format the current file.

Configuration
-------------

Blade Formatter supports all configuration options available in the underlying `blade-formatter`. You can modify these in your BladeFormatter settings by opening the Command Palette (`Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on Mac), typing `Preferences: BladeFormatter Settings`, and pressing `Enter`.

Here is the complete list of options with their default values:

```json
{
  "indent_size": 4,
  "wrap_attributes": "auto",
  "wrap_line_length": 120,
  "wrap_attributes_min_attrs": 2,
  "indent_inner_html": false,
  "end_with_newline": true,
  "end_of_line": "LF",
  "use_tabs": false,
  "sort_tailwindcss_classes": false,
  "tailwindcss_config_path": "",
  "sort_html_attributes": "none",
  "no_multiple_empty_lines": false,
  "no_php_syntax_check": false,
  "no_single_quote": false,
  "no_trailing_comma_php": false,
  "extra_liners": ["head", "body", "/html"],
  "component_prefix": ["x-", "livewire:"],
  "php_version": ""
}
```

### Option Descriptions

*   `indent_size`: The number of spaces to use for indentation (default: `4`).
*   `wrap_attributes`: The strategy to wrap HTML attributes. Choices: `"auto"`, `"force"`, `"force-aligned"`, `"force-expand-multiline"`, `"aligned-multiple"`, `"preserve"`, `"preserve-aligned"` (default: `"auto"`).
*   `wrap_line_length`: The maximum line length before wrapping is triggered (default: `120`).
*   `wrap_attributes_min_attrs`: The minimum number of HTML tag attributes required to trigger forced attribute wrapping (default: `2`).
*   `indent_inner_html`: Whether to indent the `<head>` and `<body>` sections in HTML (default: `false`).
*   `end_with_newline`: Whether to end the formatted output with a newline character (default: `true`).
*   `end_of_line`: The end of line character(s). Choices: `"LF"`, `"CRLF"` (default: `"LF"`).
*   `use_tabs`: Whether to use tabs instead of spaces for indentation (default: `false`).
*   `sort_tailwindcss_classes`: Whether to automatically sort Tailwind CSS classes (default: `false`).
*   `tailwindcss_config_path`: Path to a custom Tailwind CSS configuration file (e.g. `"tailwind.config.js"`).
*   `sort_html_attributes`: Strategy to sort HTML attributes. Choices: `"none"`, `"alphabetical"`, `"code-guide"`, `"idiomatic"`, `"vuejs"` (default: `"none"`).
*   `no_multiple_empty_lines`: Whether to merge multiple consecutive empty lines into a single blank line (default: `false`).
*   `no_php_syntax_check`: Whether to disable the PHP syntax check (default: `false`).
*   `no_single_quote`: Whether to use double quotes instead of single quotes for PHP expressions (default: `false`).
*   `no_trailing_comma_php`: Whether to disable trailing commas in PHP expressions (default: `false`).
*   `extra_liners`: List of tags that should be preceded by an extra newline (default: `["head", "body", "/html"]`).
*   `component_prefix`: List of custom prefixes for component names (default: `["x-", "livewire:"]`).
*   `php_version`: The target PHP version for syntax compatibility, e.g., `"8.0"`, `"8.1"`, `"8.2"`, `"8.3"`, `"8.4"`.


Credits
-------

Blade Formatter is based on [blade-formatter](https://github.com/jenky/blade-formatter), a PHP package that formats Blade templates. The Sublime Text package was developed by [Rahul Kadyan](https://github.com/rahulhaque) and [contributors](https://github.com/rahulhaque/sublime-blade-formatter/graphs/contributors).

License
-------

Blade Formatter is open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT).