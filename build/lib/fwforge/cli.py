import argparse
import sys
import yaml
import os
from .fw_parser import FixedWidthParser
from .writer import write_csv, write_json

def process_file(input_path, output, layout, format_type):
    column_names = [col['name'] for col in layout['columns']]
    file_parser = FixedWidthParser(layout)
    
    records = []
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if line.strip():
                records.append(file_parser.parse_line(line))
    
    try:
        if format_type == "csv":
            write_csv(records, column_names, output)
        else:
            write_json(records, output)
    finally:
        # Only close if it's a file, not stdout
        if output is not sys.stdout:
            output.close()

def main():
    parser = argparse.ArgumentParser(description="FixedWidth Forge: Legacy data parser")
    parser.add_argument("-i", "--input", required=True, help="Input file or directory")
    parser.add_argument("-s", "--schema", help="YAML schema file")
    parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("--infer", action="store_true", help="Infer schema from input file")
    args = parser.parse_args()

    if args.infer:
        # Import inside to avoid circular dependency if needed, 
        # but here it's fine.
        from .cli import infer_layout
        layout = infer_layout(args.input)
        print(yaml.dump(layout))
        return

    if not args.schema:
        parser.error("the following arguments are required: -s/--schema")

    with open(args.schema, 'r') as f:
        layout = yaml.safe_load(f)

    if os.path.isdir(args.input):
        # Batch mode
        output_dir = args.output or args.input
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for filename in os.listdir(args.input):
            if filename.endswith((".txt", ".fwf")):
                input_path = os.path.join(args.input, filename)
                output_filename = os.path.splitext(filename)[0] + "." + args.format
                output_path = os.path.join(output_dir, output_filename)
                print(f"Processing {input_path} -> {output_path}")
                with open(output_path, 'w', encoding='utf-8', newline='') as out_file:
                    process_file(input_path, out_file, layout, args.format)
    else:
        # Single file mode
        if args.output:
            output = open(args.output, 'w', encoding='utf-8', newline='')
        else:
            output = sys.stdout
        
        process_file(args.input, output, layout, args.format)

def infer_layout(filepath):
    # Moved inside or keep here, let's keep it here for simplicity
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        line = f.readline().rstrip('\n\r')
    
    columns = []
    import re
    # Simple heuristic: find contiguous non-space sequences as columns
    for match in re.finditer(r'\S+', line):
        columns.append({
            "name": f"col_{match.start()}",
            "start": match.start(),
            "length": match.end() - match.start(),
            "trim": True,
            "type": "string"
        })
    
    return {"name": "InferredLayout", "columns": columns}

if __name__ == "__main__":
    main()
