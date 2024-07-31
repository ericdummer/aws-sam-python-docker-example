#!/bin/bash

process_env_if_exists() {

    # Check if the file exists
    if [[ -f ".env" ]]; then
        echo "processing the .env file"
        . .env  
    else
        echo "No .env using local environment variables"

    fi
}
assume_aws_role() {
    ROLE_ARN=$1
    SESSION_NAME=$2

    # Use AWS STS to assume the role and get temporary security credentials
    CREDS_JSON=$(aws sts assume-role --role-arn $ROLE_ARN --role-session-name $SESSION_NAME)

    # Extract the temporary security credentials and export them as environment variables
    export AWS_ACCESS_KEY_ID=$(echo $CREDS_JSON | jq -r '.Credentials.AccessKeyId')
    export AWS_SECRET_ACCESS_KEY=$(echo $CREDS_JSON | jq -r '.Credentials.SecretAccessKey')
    export AWS_SESSION_TOKEN=$(echo $CREDS_JSON | jq -r '.Credentials.SessionToken')
    echo "Assumed IAM role under session"
}

process_env_if_exists

assume_aws_role $SAM_DEPLOY_SERVICE_ROLE_ARN "github_actions_sam_deploy"

# sam build --cached
sam deploy --stack-name $SAM_STACK_NAME\
    --parameter-overrides "SecretArn=$SAM_SECRET_ARN,DatabaseName=$SAM_DATABASE_NAME"