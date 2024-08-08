import os
import pandas as pd
import re
from tqdm import tqdm

directory = "/Users/petergrund/Documents/neurology/dysarthria_analysis/ddk_data/"

csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]

for filename in tqdm(csv_files):
    # Read the file into a pandas df
    df = pd.read_csv(os.path.join(directory, filename))

    df = df.rename(columns={
        'xmin': 'time_start',
        'xmax': 'time_stop',
        'item2_text': 'temporal_parameter',
        'item1_text': 'letter'
    })

    # Add new columns with default values
    df["study_ID"] = ""
    df["visit"] = ""
    df["eval"] = ""

    df["letter"] = df["letter"].str.replace(" ", "")

    df["letter"] = df["letter"].str.replace("c", "k")

    # Populate "study_ID" based on file name
    study_ID = filename.split('_')[0]
    df["study_ID"] = study_ID

    # Populate "visit" based on file name
    for keyword in ["visit1", "visit2", "visit3", "visit4", "visit5", "visit6", "visit7"]:
        if keyword in filename:
            df["visit"] = keyword.replace('visit', 'visit_')
            break

    # Populate "eval" based on file name
    for keyword in ["eval1", "eval2", "eval3", "eval4", "eval5"]:
        if keyword in filename:
            eval_number = re.search(r'\d+', keyword).group()
            df["eval"] = eval_number
            break

    # Write the df back to the same CSV file
    df.to_csv(os.path.join(directory, filename), index=False)