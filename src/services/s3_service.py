import logging
import os
import boto3
import io

class S3Service:

    def __init__(self, s3_client, bucket_name): 
        self._s3_client = s3_client
        self._bucket_name = bucket_name
        self.logger = logging.getLogger(__name__)  # Create a logger for your function
        self.logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))

    def upload_file_contents(self, file_contents, target_file_path):
        data = io.BytesIO(file_contents.encode('utf-8')) 
        self._s3_client.put_object(Body=data, Bucket=self._bucket_name, Key=target_file_path)

    def download_file(self, bucket_name, key, file_path):
        """Downloads a file from S3.

        Args:
            bucket_name: Name of the S3 bucket.
            key: The S3 object key (filename within the bucket).
            file_path: Path to save the downloaded file.
        """

        self._s3_client.download_file(bucket_name, key, file_path)

    def list_objects(self, bucket_name, prefix=None):
        """Lists objects in an S3 bucket.

        Args:
            bucket_name: Name of the S3 bucket.
            prefix: Optional prefix to filter results.

        Returns:
            A list of object keys.
        """

        paginator = self._s3_client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        object_keys = []
        for page in response_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    object_keys.append(obj["Key"])

        return object_keys

