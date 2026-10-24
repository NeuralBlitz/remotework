"""
Mito Converters
Data format conversions: XML, TOML, Protocol Buffers, base formats
"""

import json
import re
from typing import Dict, List, Any, Optional
from xml.etree import ElementTree as ET
from xml.dom import minidom


def dict_to_xml(data: Dict, root_name: str = "root", pretty: bool = True) -> str:
    def build_element(parent, tag, value):
        elem = ET.SubElement(parent, tag)
        if isinstance(value, dict):
            for k, v in value.items():
                build_element(elem, k, v)
        elif isinstance(value, list):
            for item in value:
                build_element(elem, "item", item)
        else:
            elem.text = str(value)

    root = ET.Element(root_name)
    for key, value in data.items():
        build_element(root, key, value)

    if pretty:
        return minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    return ET.tostring(root, encoding="unicode")


def xml_to_dict(xml_string: str) -> Dict:
    def parse_element(element):
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = parse_element(child)
        return result

    root = ET.fromstring(xml_string)
    return {root.tag: parse_element(root)}


def toml_to_dict(text: str) -> Dict[str, Any]:
    result = {}
    current_section = result

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            parts = section.split(".")
            current_section = result
            for part in parts:
                if part not in current_section:
                    current_section[part] = {}
                current_section = current_section[part]
        elif "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            if value == "true":
                value = True
            elif value == "false":
                value = False
            elif value.isdigit():
                value = int(value)
            elif re.match(r"^\d+\.\d+$", value):
                value = float(value)
            current_section[key] = value

    return result


def dict_to_toml(data: Dict, prefix: str = "") -> str:
    lines = []
    simple = {}
    nested = {}

    for key, value in data.items():
        if isinstance(value, dict):
            nested[key] = value
        else:
            simple[key] = value

    for key, value in simple.items():
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        elif isinstance(value, bool):
            lines.append(f"{key} = {'true' if value else 'false'}")
        else:
            lines.append(f"{key} = {value}")

    for key, value in nested.items():
        section = f"{prefix}.{key}" if prefix else key
        lines.append(f"\n[{section}]")
        lines.append(dict_to_toml(value, section))

    return "\n".join(lines)


def hex_to_bytes(hex_str: str) -> bytes:
    hex_str = hex_str.replace("0x", "").replace(" ", "")
    return bytes.fromhex(hex_str)


def bytes_to_hex(data: bytes, separator: str = "") -> str:
    return separator.join(f"{b:02x}" for b in data)


def int_to_binary(n: int, bits: int = 8) -> str:
    return format(n & ((1 << bits) - 1), f'0{bits}b')


def binary_to_int(binary: str) -> int:
    return int(binary, 2)


def int_to_hex(n: int, prefix: bool = True) -> str:
    return f"0x{n:x}" if prefix else f"{n:x}"


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(hex_str: str) -> tuple:
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def meters_to_feet(m: float) -> float:
    return m * 3.28084


def feet_to_meters(ft: float) -> float:
    return ft / 3.28084


def kg_to_lbs(kg: float) -> float:
    return kg * 2.20462


def lbs_to_kg(lbs: float) -> float:
    return lbs / 2.20462


def roman_to_int(s: str) -> int:
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and values[c] < values[s[i + 1]]:
            result -= values[c]
        else:
            result += values[c]
    return result


def int_to_roman(n: int) -> str:
    values = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
              (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
              (5, "V"), (4, "IV"), (1, "I")]
    result = ""
    for val, numeral in values:
        while n >= val:
            result += numeral
            n -= val
    return result


def markdown_to_plain(md: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", md, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[-*+]\s+", "• ", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
    return text.strip()


def json_to_csv(data: List[Dict]) -> str:
    import csv
    import io
    if not data:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys(), extrasaction="ignore")
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def csv_to_json(csv_text: str) -> List[Dict]:
    import csv
    import io
    return list(csv.DictReader(io.StringIO(csv_text)))


def yaml_to_json(yaml_text: str) -> str:
    try:
        import yaml
        data = yaml.safe_load(yaml_text)
        return json.dumps(data, indent=2)
    except ImportError:
        raise ImportError("PyYAML not installed")


def json_to_yaml(json_text: str) -> str:
    try:
        import yaml
        data = json.loads(json_text)
        return yaml.dump(data, default_flow_style=False)
    except ImportError:
        raise ImportError("PyYAML not installed")
