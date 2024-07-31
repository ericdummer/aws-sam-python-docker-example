import json
from datetime import datetime
from utilities.json_utils import JsonUtils 

class Event:
    time: datetime = None
    source: str = None
    detail_type: str = None
    detail: dict = None
    event_bus_name: str = None

    def __init__(self, data: dict = None) -> None:
        self.time = data.get('time', datetime.now())
        self.source = data.get('source')
        self.detail_type = data.get('detail_type')  
        self.detail = data.get('detail')
        self.event_bus_name = data.get('event_bus_name')

    def to_aws_object(self):
        return {
            'Time': self.time,
            'Source': self.source,
            'DetailType': self.detail_type,
            'Detail': JsonUtils().dumps(self.detail), # must be a json string
            'EventBusName': self.event_bus_name
        }

    def __str__(self):
        return JsonUtils().make_pretty(JsonUtils().dumps(self.to_aws_object()))