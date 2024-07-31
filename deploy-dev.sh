#!/bin/bash
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

expected_account_id="533267356524"
account_id=$(aws sts get-caller-identity --query 'Account' --output text)
if [ "$account_id" = "$expected_account_id" ]; then
    echo "AWS Account ID: $account_id"
else
    echo "Error: you cannot deploy this environment to account: $account_id"
    exit 1
fi

echo -e "${YELLOW}Building...${NC}"
sam build --config-env dev > /dev/null 2>&1 || exist $?


echo "sam deploy --config-env dev"
sam deploy --config-env dev
# Clean up docker
echo -e "${YELLOW}cleaning up docker...${NC}"
docker image prune -f > /dev/null 2>&1 
echo -e "${GREEN}DONE!!${NC}"
