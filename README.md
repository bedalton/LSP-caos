# LSP-caos

Creature's CAOS and Catalogue editing support for Sublime Text's LSP plugin

## Installation

Install the following packages in Sublime Text:
* [LSP](https://packagecontrol.io/packages/LSP) - Base LSP package
* [LSP-caos](https://packagecontrol.io/packages/LSP-caos) - This plugin
* Restart Sublime
* Set language to CAOS or Catalogue from lower right menu if not automatically set

## Configuration

Defaults can be edited by selecting `Preferences: LSP-caos Settings` from the
command palette.

### Format on save

To format your code on save add the following setting to your syntax-specific settings (Elixir in this case) and/or project files:

```json
{
  "lsp_format_on_save": true
}
```