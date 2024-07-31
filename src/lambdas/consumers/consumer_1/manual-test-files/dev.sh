#!/bin/bash

# Check if there's at least one argument provided
if [ -z "$1" ]; then
  echo "Error: Please provide a command as an argument."
  exit 1
fi

ENV_FILE=.env-dev

# Check if the file exists and is readable
if [ ! -r "$ENV_FILE" ]; then
  echo "Error: File '$ENV_FILE' does not exist or is not readable."
  exit 1
fi

# Source the file, exporting its variables
. "$ENV_FILE" 

echo "USING THE FOLOWING ENV VARIABLES"
export | grep MANUAL

# Execute the provided command
"$@"


