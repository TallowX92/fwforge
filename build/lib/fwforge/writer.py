import csv
import json
import sys

def write_csv(records, columns, output=sys.stdout):
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(records)

def write_json(records, output=sys.stdout):
    json.dump(records, output, indent=2)
