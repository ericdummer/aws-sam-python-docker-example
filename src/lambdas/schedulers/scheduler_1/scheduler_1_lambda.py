import json
import os
import logging
import time


logger = logging.getLogger(__name__)  # Create a logger for your function
logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))

def lambda_handler(event, context):
    start_time = time.time()
    message_count = 0
    
    # Do something here

    end_time = time.time()
    time_message =f"Total time: {end_time - start_time}"
    lambda_response_message = str(message_count) + " added to queue. " + time_message
    
    return {
        "statusCode": 200,
        "body": json.dumps({    
            "message":  lambda_response_message
        })
    }