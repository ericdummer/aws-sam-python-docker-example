from datetime import datetime
import json
from utilities.json_utils import JsonUtils

class HasuraEvent:

    OP_UPDATE = 'UPDATE'
    OP_INSERT = 'INSERT'
    OP_DELETE = 'DELETE'
    OP_MANUAL = 'MANUAL'

    raw: str = None
    original: dict = None

    id: str = None
    table: str = None
    schema: str = None
    trigger_name: str = None
    trace_id: str = None
    span_id: str = None 
    session_variables: dict = None
    data: dict = None
    op: str = None
    created_at: datetime = None
    delivery_info: dict = None
    current_retry: int = None
    max_retries: int = None
    data: dict = None
    new_object: dict = None
    old_object: dict = None

    # def __init__(self, db_helper: DbService):
    def __init__(self, payload):
        if type(payload) == str:
            self.load_from_json(payload)
        else:
            self.load_from_dict(payload)

    def load_from_json(self, json_string):
        self.raw = json_string
        self.original = json.loads(json_string)
        self.set_attributes(self.original)

    def load_from_dict(self, dict_object):
        self.raw = json.dumps(dict_object)  
        self.original = dict_object
        self.set_attributes(self.original)
    
    def set_attributes(self, original):
        self.id = original.get('id')
        self.table = original.get('table', {}).get('name')
        self.schema = original.get('table', {}).get('schema')
        self.trigger_name = original.get('trigger', {}).get('name')
        self.trace_id = original.get('event', {}).get('trace_context', {}).get('trace_id')
        self.span_id = original.get('event', {}).get('trace_context', {}).get('span_id')
        self.session_variables = original.get('event', {}).get('session_variables')
        self.op = original.get('event', {}).get('op')
        self.created_at = original.get('created_at')
        self.delivery_info = original.get('delivery_info')
        self.current_retry = original.get('delivery_info', {}).get('current_retry')
        self.max_retries = original.get('delivery_info', {}).get('max_retries')
        self.data = original.get('event', {}).get('data')
        self.new_object = original.get('event', {}).get('data', {}).get('new') 
        self.old_object = original.get('event', {}).get('data', {}).get('new') 

    def get_new_field(self, field_name):
        if not self.data:
            return None
        return self.data.get('new', {}).get(field_name)

    def raw_pretty(self):
        return JsonUtils().make_pretty(self.raw)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)