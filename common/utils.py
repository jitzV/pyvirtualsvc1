import json
import os

def load_json_template(template_filename, base_dir):
    # Construct the full path to the template file
    path = os.path.join(base_dir, template_filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template file not found: {path}")
    with open(path, 'r') as f:
        return json.load(f)

def load_soap_xml_files(directory):
    """
    Loads all XML files from the given directory into a dictionary.
    Key: filename (without extension)
    Value: XML content as string
    """
    xml_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                xml_data[os.path.splitext(filename)[0]] = f.read()
    return xml_data

def load_soap_xml(template_filename, base_dir):
    """
    Loads a single XML file and returns its content as a string.
    """
    path = os.path.join(base_dir, template_filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()