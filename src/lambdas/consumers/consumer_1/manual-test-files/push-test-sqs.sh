#!/bin/bash

####################
## DON'T CALL THIS FILE DIRECETLY 
## CALL ./push-message-to-stage.sh, etc
####################


if [ -z "$1" ]; then
  echo "Error: Please provide the path to the JSON file as an argument."
  exit 1
fi

JSON_FILE=$1

# Replace with your actual SQS queue URL
if [[ -z "${MANUAL_TEST_SQS_QUEUE_URL}" ]]; then
    echo "Error: Env var MANUAL_TEST_SQS_QUEUE_URL is not set or empty"
    echo "Did you run one of the following commands:"
    echo "./push-message-to-stage.sh  $JSON_FILE"
    exit 1  # Exit with an error code
fi

# Check if the JSON file exists
if [ ! -f "$JSON_FILE" ]; then
  echo "Error: JSON file not found at $JSON_FILE"
  exit 1
fi

echo "Loading JSON file: $JSON_FILE"
MESSAGE_BODY=$(jq -c '.' "$JSON_FILE")
echo "Message body: $MESSAGE_BODY"

# Ensure message was extracted
if [ -z "$MESSAGE_BODY" ]; then
  echo "Error: Could not extract 'message' from JSON file."
  exit 1
fi

echo "AWS COMMAND"
echo "------------------------------"
echo "aws sqs send-message \
    --queue-url \"$MANUAL_TEST_SQS_QUEUE_URL\" \
    --message-body \"$MESSAGE_BODY\""
echo "------------------------------"


echo "Sending the message to the SQS queue"
aws sqs send-message \
    --queue-url "$MANUAL_TEST_SQS_QUEUE_URL" \
    --message-body "$MESSAGE_BODY"