import json
import os
import boto3
import base64
import logging
from services.db_service import DbService
import uuid
from urllib.parse import urlparse


logger = logging.getLogger(__name__)  # Create a logger for your function
logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))
s3 = boto3.client('s3')

headers = {
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'GET,OPTIONS,HEAD',
    'Access-Control-Allow-Origin': '*'
}

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method', '')
    if (http_method == 'OPTIONS'):
        return {
            'statusCode': 200,
            'headers': headers 
        }

    if "uuid" not in event['pathParameters']:
        return {
            'statusCode': 404,
            'body': 'Missing document_uuid parameter',
            'headers': headers 
        }


    uuid = event['pathParameters']['document_uuid']
    if is_valid_uuid(uuid) == False:
        return {
            'statusCode': 404,
            'body': 'Invalid uuid parameter',
            'headers': headers 
        }
    bucket_name = get_bucket_name()

    logger.debug(f"S3 UPLOAD BUCKET: {bucket_name}")
    logger.debug(f"UUID: {uuid}")
    logger.debug(f"HTTP METHOD: {http_method}")

    document = get_user_document_info(uuid=uuid)
    if not document:
        return {
            'headers': headers,
            'statusCode': 404,
            'body': 'Document not found'
        }

    try:
        # Fetch the object from S3
        object_key = extract_object_key(document['path'])
        logger.debug(f"OBJECT KEY: {object_key}")
        document_data = b''
        base64_encoded = False
        content_length = None
        etag = None
        if object_key:
            if http_method == 'HEAD':
                response = s3.head_object(Bucket=bucket_name, Key=object_key)
                document_data = response['ContentLength']
                content_length = ''
                etag = response.get('ETag')
            else:
                response = s3.get_object(Bucket=bucket_name, Key=object_key)
                document_data = response['Body'].read()
                image_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
                if document_data:  
                    content_length = len(document_data)
                    etag = response.get('ETag')
                    if document['content_type'] in image_types:
                        document_data = base64.b64encode(document_data).decode('utf-8')
                        base64_encoded = True
                    if document['content_type'] == 'application/pdf':
                        document_data = document_data.decode('latin-1') 
                    if document['content_type'] == 'text/html':
                        document_data = document_data.decode('utf-8') 

        
        if not document_data:
            return {
                'headers': headers,
                'statusCode': 404,
                'body': 'Document not found'
            }
            
        headers.update({
            'ETag': etag,
            'Content-Disposition': f"attachment; filename={document['display_name']}; filename={document['filename']}",  
            'Content-Length': content_length,
            'Content-Type': document["content_type"],
            'Cache-Control': 'max-age=3600',    
            'X-Content-Type-Options': 'nosniff'
        })
        # Construct the API Gateway response
        return {
            'statusCode': 200,
            'headers': headers, 
            'body': document_data,
            'isBase64Encoded': base64_encoded  # If using base64, set this to True 
        }

    except s3.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': 'Document not found'
        }
    except Exception as e:  # Catch potential errors
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }
    

def get_bucket_name():
    override_bucket_name = os.environ.get("S3_UPLOAD_BUCKET_OVERRIDE")
    bucket_name = override_bucket_name or os.environ.get("S3_UPLOAD_BUCKET")
    if not bucket_name:
        raise Exception("S3_UPLOAD_BUCKET or S3_UPLOAD_BUCKET_OVERRIDE environment variable not set")
    return bucket_name


def get_info(uuid):
    return {
            "uuid": "",
            "content_type": "",
            "filename": "",
            "display_name": "",
            "storage_type": "",
            "path": "",
            "size": ""

    }

def extract_object_key(s3_uri):
    # path = "s3://account_files/d2e04156-6d9e-4078-8ae4-e393735a9fd0/transcript_ACTR_941_04-16-2024-163837.html"
    return s3_uri.replace("s3://", "")  # Remove the "s3://" prefix

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