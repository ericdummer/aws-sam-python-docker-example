import os
import boto3
from botocore.exceptions import ClientError
import json

class SecretsService:
    def __init__(self, secretArn):
        self.secret_arn = secretArn 
        self.client = boto3.client('secretsmanager')

    def get_secret(self):
        if not self.secret_arn:
            raise ValueError('SECRET_ARN environment variable not set.')

        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=self.secret_arn)
            if 'SecretString' in get_secret_value_response:
                return get_secret_value_response['SecretString']
            else:
                # Handle the case where the secret is stored as binary data
                return get_secret_value_response['BinarySecretData'].decode('utf-8')
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceNotFoundException':
                raise ValueError(f'Secret with ARN {self.secret_arn} not found.')
            else:
                raise error

    def get_secret_value(self, key):
        secret = self.get_secret()
        secret_data = json.loads(secret)
        return secret_data[key] 



