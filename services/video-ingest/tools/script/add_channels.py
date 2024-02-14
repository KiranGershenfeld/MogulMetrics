import csv
import subprocess
import sys

def read_csv_and_execute_command(csv_filepath):
    # Open the CSV file and read rows
    with open(csv_filepath, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row
        unique_channels = {}  # Dictionary to store unique channels based on channel_id

        # Deduplicate channels based on channel_id
        for row in csv_reader:
            channel_id, channel_name, subscriber_count = row
            unique_channels[channel_id] = (channel_name, subscriber_count)
    
    print(f'Found {len(unique_channels)} unique channels')

    # Execute command for each unique channel
    for channel_id, (channel_name, subscriber_count) in unique_channels.items():
        command = f"./add_channel.sh {channel_id} \"{channel_name}\" true {subscriber_count}"
        print(f"Adding channel: {channel_name}")
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    # Check if CSV file path is provided as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py csv_filepath")
        sys.exit(1)

    csv_filepath = sys.argv[1]  # Get CSV file path from command-line argument
    read_csv_and_execute_command(csv_filepath)