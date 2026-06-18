from pathlib import Path
from LSP.plugin import LspPlugin, OnPreStartContext
from lsp_utils import NodeManager
from sublime_lib import ResourcePath

def plugin_loaded():
    LspCaosPlugin.register()

def plugin_unloaded():
    LspCaosPlugin.unregister()


class LspCaosPlugin(LspPlugin):
    @classmethod
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath("Packages", package_name, "language-server"),
            Path("node_modules", "caos-language-server", "dist", "node", "server.js"),
            node_version_requirement=">=14",
        )
