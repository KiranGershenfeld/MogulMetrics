#!/bin/bash
#Transfers the requested file to the production server, filepath to requested server should be in relation to internal/service-name/

# Check if filename is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <filename> <destination>"
  exit 1
fi

# Check if destination directory is provided as an argument
if [ -z "$2" ]; then
  echo "Usage: $0 <filename> <destination>"
  exit 1
fi


SOURCE_DIR="../.."
DESTINATION="$2"
FILE_TO_TRANSFER="$1"

# Path to your local .env file
LOCAL_ENV_FILE="${SOURCE_DIR}/.env"

# Load variables from .env file
if [ -f "${LOCAL_ENV_FILE}" ]; then
  source "${LOCAL_ENV_FILE}"
else
  echo "Error: .env file not found."
  exit 1
fi

# Use sshpass to provide the password and copy the specified file
sshpass -p "$SERVER_PASSWORD" scp "$SOURCE_DIR/$FILE_TO_TRANSFER" "$SERVER_USERNAME@$SERVER_IP:~/$DESTINATION"

# Check the exit status of the scp command
if [ $? -eq 0 ]; then
  echo "File successfully copied to remote machine."
else
  echo "Error copying file to remote machine."
fi