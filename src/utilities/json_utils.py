import json
import difflib
from datetime import datetime, date, time

class JsonUtils:

    def dumps(self, data, **kwargs):
        kwargs.setdefault('cls', DateTimeEncoder)
        # Pass all arguments (including potentially overridden cls) to json.dumps
        return json.dumps(data, **kwargs)

    def make_pretty(self, data, sort_keys=False):
        #check if it is an instanc of a dict
        if isinstance(data, str):
            #print the list
            return json.dumps(json.loads(data), cls=DateTimeEncoder, indent=4, sort_keys=sort_keys)
        else:
            return json.dumps(data, cls=DateTimeEncoder, indent=4, sort_keys=sort_keys)

    def diff(self, original_json, new_json, exclude_keys = []):
        original_dict = json.loads(original_json)
        new_dict = json.loads(new_json)
        diff = {}
        self._diff_recursive(diff, "", original_dict, new_dict, exclude_keys)
        return json.dumps(diff)

    # Helper function for recursive diffing
    def _diff_recursive(self, diff, path, obj1, obj2, exclude_keys = []):
        if isinstance(obj1, dict) and isinstance(obj2, dict):
            for key in set(obj1.keys()) | set(obj2.keys()):
                if key in exclude_keys:
                    continue
                new_path = path + "/" + key if path else key
                if key in obj1 and key in obj2:
                    self._diff_recursive(diff, new_path, obj1[key], obj2[key], exclude_keys)
                elif key in obj1:
                    diff[new_path] = {"-": obj1[key]}  # Mark as removed
                else:
                    diff[new_path] = {"+": obj2[key]}  # Mark as added

        elif isinstance(obj1, list) and isinstance(obj2, list):
            # casting list items to a json string if they are dict objects
            obj1_items = obj1
            obj2_items = obj2
            if len(obj1) > 0 and isinstance(obj1[0], dict):
                obj1_items = [json.dumps(item, sort_keys=True) for item in obj1]

            if len(obj2) > 0 and isinstance(obj2[0], dict):
                obj2_items = [json.dumps(item, sort_keys=True) for item in obj2]

            # Use difflib for fine-grained list differences
            differ = difflib.SequenceMatcher(None, obj1_items, obj2_items)
            for tag, i1, i2, j1, j2 in differ.get_opcodes():
                new_path = path + f"[{i1}:{i2}]" if path else f"[{i1}:{i2}]"
                if tag == 'replace':
                    diff[new_path] = {"-": obj1[i1:i2], "+": obj2[j1:j2] }
                elif tag == 'delete':
                    diff[new_path] = {"-": obj1[i1:i2]}
                elif tag == 'insert':
                    diff[new_path] = {"+": obj2[j1:j2]}

        else:  # Simple value change
            if obj1 != obj2:
                diff[path] = {"-": obj1, "+": obj2}

        return diff


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime objects."""

    def default(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        
        if callable(obj.__dict__):  
            return obj.__dict__()
        
        return super().default(obj)

def json_dumps_with_datetime_conversion(data):
    """Wrapper for json.dumps that converts datetime objects to ISO format."""
    return json.dumps(data, cls=DateTimeEncoder)
