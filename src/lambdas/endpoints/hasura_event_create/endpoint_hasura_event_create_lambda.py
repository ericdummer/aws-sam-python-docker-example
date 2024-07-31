import os
import logging
import boto3
import json 
from utilities.json_utils import JsonUtils
from models.aws.event import Event as AwsEvent
from models.hasura_event import HasuraEvent
from models.account_transcript import AccountTranscript
from services.db_service import DbService
from services.hasura_event_service import HasuraEventService 


logger = logging.getLogger(__name__)  # Create a logger for your function
logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))

def lambda_handler(event, context):
    print (type(event))
    print (event)

    event_bus_name = os.environ.get("EVENT_BUS_NAME")
    if not event_bus_name:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errors": ["Missing Event Bus Name"]
            })
        }

    hasuraEvent: HasuraEvent = HasuraEvent(event.get("body", None))
    if not hasuraEvent:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errors": ["Missing or invalid body"]
            })
        }

    awsEvent: AwsEvent = HasuraEventService.build_aws_event(hasuraEvent, event_bus_name)

    eventBridge = boto3.client('events')
    try:
      awsObject = awsEvent.to_aws_object()
      response = eventBridge.put_events( Entries=[awsObject])
      if response.get("FailedEntryCount"):
        logger.error(f"Failed to send event: {response}")
    except eventBridge.exceptions.ClientError as e:
        logger.error(f"Error sending event: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errors": ["Error sending event"]
            })
        }

    message = f"Hasura Event with source {hasuraEvent.trigger_name}added to EventBridge"
    return {
        "statusCode": 200,
        "body": json.dumps({    
            "message": message
        })
    }
# todo move this to the target