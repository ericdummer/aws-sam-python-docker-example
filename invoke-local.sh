#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check if there's at least one argument provided
if [ -z "$1" ]; then
  echo "Error: Please provide a Resource to ."
  exit 1
fi

echo -e "${YELLOW}Building...${NC}"


# check if samconfig.local.toml exists
if [ -f "samconfig.local.toml" ]; then
  echo -e "${YELLOW}using samconfig.local.toml${NC}" 
  sam build --config-file samconfig.local.toml> /dev/null 2>&1 || exist $?
else
  sam build > /dev/null 2>&1 || exist $?
fi



if [ -f "samconfig.local.toml" ]; then
  echo "sam local invoke --config-file samconfig.local.toml $@"
  sam local invoke --config-file samconfig.local.toml "$@" 
else
  echo "sam local invoke $@"
  sam local invoke "$@" 
fi

formatted_datetime=$(date +"%Y-%m-%d %I:%M:%S %p")
echo -e "${YELLOW}completed at ${GREEN}$formatted_datetime${NC}"

echo -e "${YELLOW}cleaning up docker...${NC}"

docker image prune -f > /dev/null 2>&1 
echo -e "${GREEN}DONE!!${NC}"
exit 0
