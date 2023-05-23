import os
import pandas as pd

def clean_data(directory, output_directory):
    filename = '**.csv'
    output_filename = 'derived_data.csv'
    
    # Check if the raw data file exists
    if not os.path.isfile(os.path.join(directory, filename)):
        print(f"Error: File {filename} does not exist in directory {directory}")
        exit(1)

    # Load the raw data
    df_raw = pd.read_csv(os.path.join(directory, filename))

    # Remove rows where 'Document Type' is NaN
    df_raw = df_raw[df_raw['Document Type'].notna()]

    # Filter the dataframe to only 'Text Only Transcript'
    df_derived = df_raw[df_raw['Text Only Transcript'].notna()]

    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Save the derived data
    df_derived.to_csv(os.path.join(output_directory, output_filename), index=False)


if __name__ == '__main__':
    raw_data_directory = "data/raw"  # Directory where the raw data is located
    derived_data_directory = "data/derived"  # Directory to save the cleaned data
    clean_data(raw_data_directory, derived_data_directory)
