import sublime
from lsp_utils import NpmClientHandler
import os

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
