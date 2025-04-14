import json
import os

def load_json_template(template_filename):
    path = os.path.join(os.path.dirname(template_filename), template_filename)
    with open(path, 'r') as f:
        return json.load(f)