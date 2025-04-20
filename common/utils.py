import json
import os

def load_json_template(template_filename, base_dir):
    # Construct the full path to the template file
    path = os.path.join(base_dir, template_filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template file not found: {path}")
    with open(path, 'r') as f:
        return json.load(f)