import pandas as pd

def deduplicate_csv(filepath):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)

    # Deduplicate based on the 'channel_id' column
    deduplicated_df = df.drop_duplicates(subset=['channel_id'])

    # Write the deduplicated DataFrame to output_dedup.csv
    deduplicated_df.to_csv('output_dedup.csv', index=False)

