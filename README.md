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

You can format your Blade templates by using the `Format: Blade` command. Here's how to do it:

1.  Open a Blade template file
2.  Press `Ctrl+Shift+P` on Windows or `Cmd+Shift+P` on Mac to open the command palette
3.  Type `Blade Formatter` and press `Enter`

Alternatively, you can use the keyboard shortcut `Ctrl+Alt+B` on Windows or `Cmd+Alt+B` on Mac to format the current file.

Configuration
-------------

Blade Formatter supports a few configuration options that you can modify in your Sublime Text's settings. To access the settings, open the command palette, type `Preferences: Settings` and press `Enter`. Then, add the following options to your settings file:

```json
{
  "indent_size": 4,
  "wrap_attributes": "auto",
  "wrap_line_length": 120,
  "end_with_newline": true,
  "end_of_line": "LF",
  "sort_tailwindcss_classes": true,
  "sort_html_attributes": "none",
  "no_multiple_empty_lines": false,
  "no_php_syntax_check": false
}
```

Here's what each option does:

*   `indent_size`: The number of spaces to use for indentation (default: 4)
*   `wrap_attributes`: The maximum line length before wrapping long lines (default: 120)
*   `wrap_line_length`: Whether to align variables in control structures (default: true)
*   `blade_formatter_space_after_control_structures`: Whether to add a space after control structures (default: true)
*   `blade_formatter_space_after_echos`: Whether to add a space after echos (default: false)
*   `blade_formatter_space_between_arguments`: Whether to add a space between function arguments (default: true)
*   `blade_formatter_trailing_commas`: Whether to add trailing commas to arrays and function calls (default: true)

Credits
-------

Blade Formatter is based on [blade-formatter](https://github.com/jenky/blade-formatter), a PHP package that formats Blade templates. The Sublime Text package was developed by [Rahul Kadyan](https://github.com/rahulhaque) and [contributors](https://github.com/rahulhaque/sublime-blade-formatter/graphs/contributors).

License
-------

Blade Formatter is open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT).