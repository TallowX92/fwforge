# FixedWidth Forge: Logistics Data Parser

Stop guessing what those legacy mainframe/ERP flat files contain. **FixedWidth Forge (FW Forge)** brings high-speed data previewing directly into your VS Code workflow.

Designed specifically for logistics, warehousing, and supply chain data, this tool parses complex fixed-width flat files (`.txt`, `.fwf`) and displays them as clean, readable tables based on your schema.

## Features
- **Instant Preview**: Right-click any text file in the explorer to preview it as a table.
- **Schema-Driven**: Uses your `layout.yaml` to parse files accurately.
- **Configurable**: Define the path to your `fwforge` CLI if it's not in your global `PATH`.
- **Logistics Optimized**: Perfect for parsing EDI-850, COBOL exports, shipment manifests, and AS/400 reports.

## Getting Started

### 1. Prerequisites
You must have the **FW Forge CLI** installed:
```bash
pip install fwforge
```

### 2. Configure Your Layout
Place a `layout.yaml` file in the same directory as the data file you want to preview. Example:

```yaml
name: "Shipment-Manifest"
columns:
  - name: "carrier_code"
    start: 0
    length: 5
    type: "string"
  - name: "weight"
    start: 20
    length: 10
    type: "float"
```

### 3. Usage
- Right-click any `.txt` or `.fwf` file in the VS Code Explorer.
- Select **"FW Forge: Preview as Table"**.
- If a `layout.yaml` is not found, you will be prompted to select one.

## Configuration
If the `fwforge` CLI is not in your global path, you can set the path in your VS Code settings:
`"fwforge.cliPath": "/absolute/path/to/your/fwforge/bin/fwforge"`

---
*Built for logistics engineers who need data visibility, not enterprise bloat.*
