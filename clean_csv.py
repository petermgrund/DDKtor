import os
import pandas as pd
import re
from tqdm import tqdm

directory = "/Users/petergrund/Documents/neurology/dysarthria_analysis/ddk_data/"

csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]

for filename in tqdm(csv_files):
    # Read the file into a pandas DataFrame
    df = pd.read_csv(os.path.join(directory, filename))

    df = df.rename(columns={
        'xmin': 'time_start',
        'xmax': 'time_stop',
        'item2_text': 'temporal_parameter',
        'item1_text': 'letter'
    })

    # Add new columns with default values
    df["study_ID"] = ""
    df["brain_side"] = ""
    df["visit"] = ""
    df["mA"] = ""
    df["configuration"] = ""

    df["letter"] = df["letter"].str.replace(" ", "")

    df["letter"] = df["letter"].str.replace("c", "k")

    # Update "study_ID" and "brain_side" based on the characters of the file name
    study_ID = filename.split('_')[0]
    df["study_ID"] = study_ID

    brain_side = filename.split('_')[1]
    df["brain_side"] = brain_side

    # Update "visit" based on the presence of certain keywords in the file name
    for keyword in ["Baseline", "6mo", "12mo", "18mo", "24mo"]:
        if keyword in filename:
            df["visit"] = keyword
            break

    # Update "mA" based on the presence of a pattern in the file name
    mA_match = re.search(r'(\d+\.\d+)mA', filename)
    if mA_match:
        df["mA"] = mA_match.group(1)
    
    configuration_match = re.search(r'(Baseline|6mo|12mo|18mo|24mo)_(\d{2})', filename)
    if configuration_match:
        df["configuration"] = configuration_match.group(2)

    # Write the DataFrame back to the CSV file
    df.to_csv(os.path.join(directory, filename), index=False)