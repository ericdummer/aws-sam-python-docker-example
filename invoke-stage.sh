#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


expected_account_id="242761325242"
account_id=$(aws sts get-caller-identity --query 'Account' --output text)
if [ "$account_id" = "$expected_account_id" ]; then
    echo "AWS Account ID: $account_id"
else
    echo "Error: you cannot invoke this environment on account: $account_id"
    exit 1
fi

build_and_deploy=false  # Initialize a flag variable

# Process arguments 
while [[ $# -gt 0 ]]; do  # Loop while there are arguments
  case "$1" in
    --build-and-deploy)
      build_and_deploy=true
      shift # Remove the --build-and-deploy flag
      ;;
    *)
    break # Exit the loop with the remainder of the arguments in $@
  esac
done


# Conditional build and deploy
if $build_and_deploy; then 

  echo -e "${YELLOW}Building...${NC}"
  sam build > /dev/null 2>&1 || exist $?
  echo -e "${YELLOW}deploying!!${NC}"
  sam deploy || exist $?
fi

echo "sam remote invoke --config-env stage $@"
START_INVOKE=$(date +%s)
sam remote invoke --config-env stage "$@" 
END_INVOKE=$(date +%s)
INVOKE_DURATION=$((END_INVOKE - START_INVOKE))
echo "\n"
echo -e "${YELLOW}Invocation took ${GREEN}${INVOKE_DURATION}${YELLOW} seconds${NC}"

formatted_datetime=$(date +"%Y-%m-%d %I:%M:%S %p")
echo -e "${YELLOW}completed at ${GREEN}$formatted_datetime${NC}"