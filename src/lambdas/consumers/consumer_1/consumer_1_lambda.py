import json
from pathlib import Path
import os
import logging
import time

logger = logging.getLogger(__name__)  # Create a logger for your function
logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))

def lambda_handler(event, context):
    logger.debug("EVENT:")
    logger.debug("\n" + json.dumps(event, indent=4, sort_keys=False))
    invocation_id = context.aws_request_id

    failed_messages = []
    start_time = time.time()
    for record in event['Records']:
        try:
            if 'body' not in record:
                raise KeyError("Event appears to be malformed' please provide a body")
            body = json.loads(record['body'])
            # logger.debug("\n" + json.dumps(body, indent=4, sort_keys=False))
            errors = process_message(body, invocation_id)
            #TODO HANDLE ERRORS
            if len(errors) > 0:
                account_uuid = body.get("account_uuid")
                error_message = f"Failed for transcript: {account_uuid}"
                for e in errors:
                    logger.error(e + " ACCOUNT_UUID: " + account_uuid)
                failed_messages.append(error_message)
        except Exception as e:
            raise e
        
    number_record = len(event["Records"]) - len(failed_messages)
    end_time = time.time()
    time_message =f"Total time: {end_time - start_time}"
    message = f"{number_record} record(s) processed. {len(failed_messages)} failed. {time_message}"
    return {
        "statusCode": 200,
        "body": json.dumps({    
            "message": message
        })
    }

def process_message(message, invocation_id):   
    # logger.debug("\n" + json.dumps(message, indent=4))
    return []

def print_context_info(context):
    print("CONTEXT:")
    context_data = {
        "request_id": context.aws_request_id,
        "function_name": context.function_name,
        "log_group_name": context.log_group_name,
        "log_stream_name": context.log_stream_name,
        "function_name": context.function_name,
        "memory_limit_in_mb": context.memory_limit_in_mb, 
        "function_version": context.function_version,
        "invoked_function_arn": context.invoked_function_arn,
        "client_context": context.client_context,
        #cognito stuff missing, but we're currently not using it
    }
    print(json.dumps(context_data, indent=4, sort_keys=False))
