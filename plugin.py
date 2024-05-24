from __future__ import annotations

import json

import sublime

import sublime_plugin

import os

import re

from lsp_utils import NpmClientHandler

assert __package__

global plugin_path
plugin_path = os.path.join(sublime.packages_path(), "LSP-caos")

global last_color_scheme
last_color_scheme = None


def get_color_scheme():
    preferences = sublime.load_settings('Preferences.sublime-settings')
    if preferences is None:
        return None
    scheme = preferences.get('color_scheme').split(os.path.sep)
    if scheme is None:
        return None
    if scheme[-1] == preferences.get('color_scheme'):
        scheme = preferences.get('color_scheme').split('/')
    filename, file_ext = os.path.splitext(scheme[-1])
    return filename


def create_color_scheme():

    global plugin_path
    global last_color_scheme
    
    current_color_scheme = get_color_scheme()

    if current_color_scheme is None:
        return

    if current_color_scheme == last_color_scheme:
        return

    last_color_scheme = current_color_scheme

    scheme_name = os.path.splitext(os.path.basename(current_color_scheme))[0]
    scheme_dest_path = os.path.join(plugin_path, scheme_name + os.extsep + "sublime-color-scheme")

    settings = sublime.load_settings("LSP-caos.sublime-settings").get("settings")

    rules = []

    style = settings.get("caosScript.theme.caos2pray.unofficial_tags.style")
    if style is not None and style.strip():
        rules.append({
            "name": "CAOS2Pray User Tags",
            "scope": "keyword.control.unofficial_tag.caos",
            "font_style": style,
        })

    style = settings.get("caosScript.theme.caos2pray.official_tags.style")
    if style is not None and style.strip():
        rules.append({
            "name": "CAOS2Pray Official Tags",
            "scope": "keyword.control.official_tag.caos",
            "font_style": style,
        })

    # COMMANDS
    style = settings.get("caosScript.theme.caos2pray.command.style")
    if style is not None and style.strip():
        rules.append({
            "name": "CAOS2Pray Command",
            "scope": "keyword.control.command.caos",
            "font_style": style,
        })

    # Agent Name
    style = settings.get("caosScript.theme.caos2pray.command.agent-name.style")
    if style is not None and style.strip():
        rules.append({
            "name": "CAOS2Pray Agent Name Command",
            "scope": "keyword.control.command.agent-name.caos",
            "font_style": style,
        })

    if rules:
        scheme = {
            "rules": rules
        }
        template_contents = json.dumps(
            scheme,
            indent=4
        )
        with os.open(scheme_dest_path, "w") as f:
            f.write(template_contents)
    elif os.path.exists(scheme_dest_path):
        os.remove(scheme_dest_path)


def remove_generated_color_schemes():

    global plugin_path
    color_schemes = sublime.find_resources('*.sublime-color-scheme')
    current_color_scheme = re.escape(get_color_scheme())

    for colorScheme in color_schemes:

        is_current_theme = re.match(f"Packages/LSP-caos/({current_color_scheme}\\.sublime-color-scheme)", colorScheme)

        if is_current_theme is not None:
            continue

        match = re.match('Packages/LSP-caos/(.+\\.sublime-color-scheme)', colorScheme)

        if match is not None:
            f = os.path.join(plugin_path, match.group(1))

            if os.path.exists(f):
                os.remove(f)


def update_plugin_settings():
    """
    Watch for plugin settings changes
    """
    global last_color_scheme
    remove_generated_color_schemes()
    last_color_scheme = None
    create_color_scheme()


def plugin_loaded() -> None:
    LspCaosPlugin.setup()
    settings = sublime.load_settings('LSP-caos.sublime-settings')
    settings.add_on_change('plugin.lsp-caos', update_plugin_settings)

    settings = sublime.load_settings("Preferences.sublime-settings")
    settings.add_on_change("plugin.lsp-caos", update_plugin_settings)

    global plugin_path
    os.makedirs(plugin_path, exist_ok=True)
    create_color_scheme()


def plugin_unloaded() -> None:
    LspCaosPlugin.cleanup()
    settings = sublime.load_settings('LSP-caos.sublime-settings')
    settings.clear_on_change('plugin.lsp-caos')

    settings = sublime.load_settings("Preferences.sublime-settings")
    settings.clear_on_change('plugin.lsp-caos')
    

class LspCaosPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "node_modules",
        "caos-language-server",
        "dist",
        "node",
        "server.js",
    )

    @classmethod
    def required_node_version(cls) -> str:
        """
        Testing playground at https://semver.npmjs.com
        And `0.0.0` means "no restrictions".
        """
        return ">=14"