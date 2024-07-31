#!/bin/bash

# Load environment variables (make sure this aligns with your file path)
source .env-auth0

if [ -z "$AUTH0_CLIENT_ID" ] || [ -z "$AUTH0_CLIENT_SECRET" ] || [ -z "$AUTH0_AUDIENCE" ]; then
    echo "Error: AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, and AUTH0_AUDIENCE environment variables are required."
    exit 1
fi

# Construct JSON data
data=$(jq -n \
        --arg AUTH0_CLIENT_ID "$AUTH0_CLIENT_ID" \
        --arg AUTH0_CLIENT_SECRET "$AUTH0_CLIENT_SECRET" \
        --arg AUTH0_AUDIENCE "$AUTH0_AUDIENCE" \
        '{client_id: $AUTH0_CLIENT_ID, client_secret: $AUTH0_CLIENT_SECRET, audience: $AUTH0_AUDIENCE, grant_type: "client_credentials"}')

# Make the API call and extract Bearer token
response=$(curl --request POST \
                --url $AUTH0_GET_BEARER_URL \
                --header 'content-type: application/json' \
                --data "$data")

bearer_token=$(echo "$response" | jq -r '.access_token')

json_data=$(jq -n \
        --arg type "REQUEST" \
        --arg auth_token "Bearer $bearer_token" \
        --arg method_arn "$methodArn" \
        '{"type": $type, "identitySource": [ $auth_token ], "routeArn": "arn:aws:execute-api:us-east-1:123456789012:api-id/stage-name/HTTP-Verb/resource-path"}')

# Write the JSON data to a file
echo "$json_data" 
echo "$json_data" > events/authorizers/auth0/event-request-temp.json 

