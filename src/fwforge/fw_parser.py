from typing import Any, Dict, List

class FixedWidthParser:
    def __init__(self, layout: Dict):
        self.layout = layout
        self.columns = layout.get('columns', [])

    def parse_line(self, line: str) -> Dict[str, Any]:
        record = {}
        for col in self.columns:
            start = col.get('start', 0)
            # Support both length and end
            if 'length' in col:
                end = start + col['length']
            elif 'end' in col:
                end = col['end']
            else:
                end = start # Default to zero-length if neither provided
                
            trim = col.get('trim', True)
            
            if end > len(line):
                val = line[start:].strip() if trim else line[start:]
            else:
                val = line[start:end]
                if trim:
                    val = val.strip()
            
            # Basic type conversion
            record[col['name']] = self._cast_value(val, col.get('type', 'string'))
        
        return record

    def _cast_value(self, value: str, col_type: str) -> Any:
        if not value:
            return None if col_type in ('int', 'float') else ""
        
        try:
            if col_type == 'int':
                return int(value)
            elif col_type == 'float':
                return float(value)
            elif col_type == 'string':
                return value
        except ValueError:
            pass  # fallback to string
        return value