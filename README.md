# FixedWidth Forge

[![PyPI version](https://img.shields.io/pypi/v/fwforge.svg)](https://pypi.org/project/fwforge/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fwforge)](https://pypi.org/project/fwforge/)
[![GitHub](https://img.shields.io/github/license/Devotall/fwforge)](https://github.com/Devotall/fwforge)

**Parse legacy fixed-width files from logistics, warehouses, ERP systems, and mainframes — instantly.**

Turn messy carrier reports, shipment manifests, and COBOL exports into clean CSV or JSON with a simple YAML schema.

## Why Logistics & Supply Chain?
Legacy formats like **fixed-width flat files**, **EDI**, and proprietary mainframes are the glue of the supply chain. `fwforge` provides the bridge to modern data pipelines without the enterprise bloat.

## Features
- **Schema-Driven**: Define column layouts in YAML. Supports `start+length` or `start+end` positions.
- **Ultra-Fast**: Built on Python principles for rapid parsing of multi-gigabyte flat files.
- **Batch Processing**: Process entire directories of manifest exports with one command.
- **Inference Engine**: Use `--infer` to automatically generate a baseline schema from a sample data file.
- **Clean Output**: Transform legacy data to clean CSV or JSON with built-in type casting.

## Installation (Free / Open Source)

```bash
pip install fwforge
```

Install from source (latest dev):

```bash
pip install git+https://github.com/Devotall/fwforge.git
```

**Looking for the commercial Pro binary?**  
See [fwforge-pro/](https://github.com/Devotall/fwforge/tree/main/fwforge-pro) for the standalone high-performance version with multi-threading, audit logs, and enterprise features. One-time purchase or annual license (no PyPI, no subscriptions for the binary itself).

## Quick Start

### 1. Infer a schema
Start from scratch with a sample file:
```bash
fwforge --infer -i data.txt > my-layout.yaml
```

### 2. Parse data
Convert legacy data to CSV (using the included sample):
```bash
fwforge -i data.txt -s layout.yaml -f csv -o output.csv
cat output.csv
```

### 3. Batch process a folder
```bash
fwforge -i ./daily_manifests/ -s manifest.yaml -f json
```

## VS Code Extension (Alpha)
Preview legacy mainframe data as interactive tables directly in VS Code.

- Located in: `vscode-extension/`
- Supports context-menu "FW Forge: Preview as Table" for `.txt` and `.fwf` files (and similar).
- Visualizes raw mainframe output using your custom YAML schemas.
- Requires the `fwforge` CLI in PATH (configurable via `fwforge.cliPath` setting).
- **Funnel for Pro**: Automatically detects files >50MB and offers an upgrade prompt to the high-speed Pro binary.

### Installation
```bash
cd fwforge/vscode-extension
npm install -g @vscode/vsce
vsce package
code --install-extension fixedwidth-forge-0.1.0.vsix
```

The extension runs the CLI to parse and renders a clean HTML table in a webview.

## Free vs Pro

- **Free (PyPI + open source)**: `pip install fwforge`. Great for most users.
- **Pro (commercial binary)**: Standalone `fwforge-pro` with multi-threading, auto-repair, audit logs, and pre-built schemas. See `fwforge-pro/` and the [landing page](fwforge-pro/landing/index.html).

This follows an "invisible sales" model: the extension and docs do the selling for power users who hit real scale.

### Invisible Sales / Long-Tail Strategy
- Document specific formats: "How to parse SAP fixed-width to CSV", "AS/400 flat file parsing", etc. (add pages to GitHub Wiki or /docs).
- List supported formats in the VS Code Marketplace description.
- Answer GitHub issues in related logistics/EDI projects with links to fwforge.

## Example Schema (`layout.yaml`)
```yaml
name: "Freight-Manifest-v1"
columns:
  - name: "carrier_code"
    start: 0
    length: 5
    trim: true
    type: "string"
  - name: "weight"
    start: 20
    length: 10
    trim: true
    type: "float"
```

## Development

```bash
git clone https://github.com/Devotall/fwforge.git
cd fwforge
uv sync
uv run pytest -v

# Run the CLI
uv run fwforge --help
```

## Roadmap

- More robust type casting (dates, currency, custom)
- Schema validation + strict mode
- Better inference (header detection, multi-line records)
- Performance / memory improvements for GB+ files
- Standalone binary releases
- Expanded output formats (parquet, etc.)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes.
