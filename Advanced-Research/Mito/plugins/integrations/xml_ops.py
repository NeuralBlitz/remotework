"""
XML Operations Plugin
Parse, query, validate, and transform XML documents.
"""
import logging
from typing import Any, Dict, List
from xml.etree import ElementTree as ET

logger = logging.getLogger("mito.plugins.xml_ops")


def xml_parse_cmd(file_path: str = "", data: str = "") -> Dict:
    if file_path:
        tree = ET.parse(file_path)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)
    return {"root_tag": root.tag, "text": root.text, "children": [child.tag for child in root]}


def xml_to_dict_cmd(file_path: str = "", data: str = "") -> Dict:
    if file_path:
        tree = ET.parse(file_path)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)

    def elem_to_dict(elem):
        result = {"tag": elem.tag}
        if elem.attrib:
            result["attributes"] = dict(elem.attrib)
        if elem.text and elem.text.strip():
            result["text"] = elem.text.strip()
        children = [elem_to_dict(child) for child in elem]
        if children:
            result["children"] = children
        return result
    return elem_to_dict(root)


def xml_xpath_cmd(file_path: str = "", xpath: str = "", data: str = "") -> List[Dict]:
    if file_path:
        tree = ET.parse(file_path)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)
    ns = {"": ""}
    results = root.findall(xpath, ns) or []
    return {"results": [elem_to_dict(r) for r in results], "count": len(results)}


def xml_validate_cmd(file_path: str = "", xsd_path: str = "") -> Dict:
    try:
        tree = ET.parse(file_path)
        if xsd_path:
            schema = ET.XMLSchema(ET.parse(xsd_path))
            schema.assertValid(tree)
        return {"valid": True, "file": file_path}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def xml_create_cmd(root_tag: str = "", children: str = "") -> str:
    import json
    root = ET.Element(root_tag)
    child_list = json.loads(children) if children else []
    for child in child_list:
        c = ET.SubElement(root, child.get("tag", "item"))
        c.text = child.get("text", "")
        for k, v in child.get("attributes", {}).items():
            c.set(k, v)
    return ET.tostring(root, encoding="unicode")


def xml_transform_cmd(file_path: str = "", xslt_path: str = "") -> str:
    import json
    if not xslt_path:
        return ET.tostring(ET.parse(file_path).getroot(), encoding="unicode")
    tree = ET.parse(file_path)
    xslt = ET.parse(xslt_path)
    result = ET.XSLT(xslt)(tree)
    return str(result)


def register(plugin):
    plugin.register_command("parse", xml_parse_cmd)
    plugin.register_command("to_dict", xml_to_dict_cmd)
    plugin.register_command("xpath", xml_xpath_cmd)
    plugin.register_command("validate", xml_validate_cmd)
    plugin.register_command("create", xml_create_cmd)
    plugin.register_command("transform", xml_transform_cmd)


PLUGIN_METADATA = {
    "name": "xml_ops", "version": "1.0.0",
    "description": "XML parsing, XPath queries, validation, and transformation",
    "author": "Mito Team", "license": "MIT",
    "tags": ["xml", "data", "parsing", "utilities"],
    "dependencies": [], "permissions": ["read_files"],
    "min_mito_version": "1.0.1",
}

xml_ops_plugin = {"metadata": PLUGIN_METADATA, "register": register}
