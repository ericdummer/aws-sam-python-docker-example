#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Building...${NC}"


# check if samconfig.local.toml exists
if [ -f "samconfig.local.toml" ]; then
  echo -e "${YELLOW}using samconfig.local.toml${NC}" 
  sam build --config-file samconfig.local.toml> /dev/null 2>&1 || exist $?
else
  sam build > /dev/null 2>&1 || exist $?
fi



if [ -f "samconfig.local.toml" ]; then
  echo "sam local invoke --config-file samconfig.local.toml"
  sam local start-api --config-file samconfig.local.toml
else
  echo "sam local invoke"
  sam local start-api
fi

echo -e "${YELLOW}cleaning up docker...${NC}"

docker image prune -f > /dev/null 2>&1 
echo -e "${GREEN}DONE!!${NC}"
exit 0
