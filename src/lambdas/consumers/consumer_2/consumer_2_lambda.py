import json
from utilities.string_utils import is_uuid
from services.db_service import DbService


def lambda_handler(event, context):
    validation_errors = []

    if (event.get('detail') is None):
        message = "Missing or invalid body"
        return {
            'statusCode': 400,
            'body': message
        }

    account_uuid = ''
    if not account_uuid:
        validation_errors.append("Missing of invalid account_uuid")

    if validation_errors:
        return {
            "statusCode": 400,
            "body": json.dumps({    
                "errors": validation_errors
            })
        }
    message = f"New Account created for Account UUID: {account_uuid}" 

    # Return a success response
    return {
        'statusCode': 200,
        'body': message
    }