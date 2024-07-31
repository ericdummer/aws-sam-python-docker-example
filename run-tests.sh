#!/bin/bash
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


# Get the test name parameter (if not provided, default to just "tests")
TEST_NAME="${1:-tests}"

# Build the Docker image
echo -e "${YELLOW}building docker${NC}"
if ! docker build -f Dockerfile.test -t my-app-test .; then
  echo "Docker build failed"
  exit 1
fi

# Run pytest within the container, passing the test name
# -s allows standard out to be printed to the terminal
docker run --rm -it my-app-test pytest -s -k "$TEST_NAME" 


echo -e "${YELLOW}pruning docker${NC}"
docker image prune -f > /dev/null 2>&1 
echo -e "${GREEN}DONE!!${NC}"
