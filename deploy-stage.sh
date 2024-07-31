#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


expected_account_id="242761325242"
account_id=$(aws sts get-caller-identity --query 'Account' --output text)
if [ "$account_id" = "$expected_account_id" ]; then
    echo "AWS Account ID: $account_id"
else
    echo "Error: you cannot deploy this environment to account: $account_id"
    exit 1
fi

echo -e "${YELLOW}Building...${NC}"
START_BUILD=$(date +%s)
sam validate && sam build --config-env stage > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Error during SAM build! Run sam validate and sam build for details"
    exit 1
       # Handle the error, perhaps log detailed output somewhere
fi
END_BUILD=$(date +%s)
BUILD_DURATION=$((END_BUILD - START_BUILD))
echo -e "${YELLOW}Build took ${GREEN}${BUILD_DURATION}${YELLOW} seconds${NC}"


echo "sam deploy --config-env stage"
START_DEPLOY=$(date +%s)
sam deploy --config-env stage
END_DEPLOY=$(date +%s)
DEPLOY_DURATION=$((END_DEPLOY - START_DEPLOY))
if [ $? -ne 0 ]; then
    echo -e "${RED}Error during SAM deploy!${NC}"
fi
echo -e "${YELLOW}Execution took ${GREEN}${DEPLOY_DURATION}${YELLOW} seconds${NC}"
formatted_datetime=$(date +"%Y-%m-%d %I:%M:%S %p")
echo -e "${YELLOW}completed at ${GREEN}$formatted_datetime${NC}"


# Clean up docker
echo -e "${YELLOW}cleaning up docker...${NC}"
# docker image prune -f > /dev/null 2>&1 
echo -e "${GREEN}DONE!!${NC}"
exit 0