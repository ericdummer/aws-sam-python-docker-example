import logging 
import os
from services.db_service import DbService  # Assuming the previous class is available
from utilities.json_utils import JsonUtils  # Assuming the previous class is available
from models.hasura_event import HasuraEvent
from models.aws.event import Event as AwsEvent

class HasuraEventService:

    DETAIL_TYPE = 'hasura_event'

    def __init__(self):
        self.logger = logging.getLogger(__name__)  # Create a logger for your function
        print(__name__)
        self.logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))
    
    def build_aws_event(hasura_event: HasuraEvent, event_bus_name: str):
        """
        Build an AWS Event object from a HasuraEvent object.

        Args:
            hasura_event (HasuraEvent): The HasuraEvent object to build the AWS Event from.

        Returns:
            AwsEvent: The AWS Event object built from the HasuraEvent object.
        """
        return AwsEvent({
            'source': hasura_event.trigger_name,
            'detail_type': HasuraEventService.DETAIL_TYPE,
            'detail': hasura_event.original,
            'event_bus_name': event_bus_name
        })

    def has_material_changes(hasura_event: HasuraEvent, material_keys: list = None, ignore_delete = True):
        """
        Check if the material keys in the object have changed.

        Args:
            hasura_event (HasuraEvent): The HasuraEvent object to check.
            material_keys (list, optional): The list of material keys to check. Defaults to None.

        Returns:
            bool: True if the material keys have changed, False otherwise.
        """
        needed = hasura_event.op == HasuraEvent.OP_DELETE and not ignore_delete
        # Alaway run on a manual execution
        needed = needed or hasura_event.op == HasuraEvent.OP_MANUAL or hasura_event.op == HasuraEvent.OP_INSERT
        # skip if we already know it's needed
        if not needed and hasura_event.op == HasuraEvent.OP_UPDATE:
            if material_keys:
                for key in material_keys:
                    new_key_value = HasuraEventService._get_nested_value(hasura_event.new_object, key)
                    old_key_value = HasuraEventService._get_nested_value(hasura_event.old_object, key)
                    if new_key_value != old_key_value:
                        needed = True
                        print (f"materially changed - needed: {needed}")
                        break
        return needed 
    
    #THESE COULD MOVE TO A DICTIONARY UTILS CLASS
    def _get_nested_value(d, key):
        """
        Recursively search for the FIRST key in nested dictionaries and return its value.

        Args:
            d (dict): The dictionary to search.
            key (str): The key to search for.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        if key in d:
            return d[key]
        for k, v in d.items():
            if isinstance(v, dict):
                result = HasuraEventService._get_nested_value(v, key)
                if result is not None:
                    return HasuraEventService._sort_nested_dict(result)
        return None
    
    def _sort_nested_dict(d):
        """
        Recursively sorts the keys of a nested dictionary.

        Args:
            d (dict): The dictionary to sort.

        Returns:
            dict: A new dictionary with sorted keys.
        """
        if not isinstance(d, dict):
            return d  # Base case: if d is not a dictionary, return it as is

        sorted_dict = {}
        for key in sorted(d.keys()):
            sorted_dict[key] = HasuraEventService._sort_nested_dict(d[key])
        return sorted_dict
