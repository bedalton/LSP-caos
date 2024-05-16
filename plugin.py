from __future__ import annotations

import os

from lsp_utils import NpmClientHandler

assert __package__


def plugin_loaded() -> None:
    LspCaosPlugin.setup()


def plugin_unloaded() -> None:
    LspCaosPlugin.cleanup()


class LspCaosPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "node_modules",
        "@creatures-lsp/caos-language-server",
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