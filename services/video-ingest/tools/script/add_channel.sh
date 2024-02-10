#!/bin/bash

# Check if required arguments are provided
[ -z "$1" ] && [ -z "$2" ] && [ -z "$3" ] && [ -z "$4" ] && { echo "Usage: $0 <channel_id> <channel_name> <subscribe> <subscriberCount>"; exit 1; }

# Define variables
CONTAINER_NAME="local-trending"
COMMAND="video-ingest channel add --channel_id $1 --channel_name $2 --subscribe $3 --subscriberCount $4"

# Execute the command inside the Docker container
docker exec -it "$CONTAINER_NAME" /bin/sh -c "$COMMAND"