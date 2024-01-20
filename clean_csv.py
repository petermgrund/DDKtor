import os
import pandas as pd
import re

directory = '../dysarthria_analysis/ddk_data/'

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Rename the file to remove the first underscore
        new_filename = filename.replace("_", "", 1)
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

        # Read the file into a pandas DataFrame
        df = pd.read_csv(os.path.join(directory, new_filename))

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
        df["ordinality"] = ""

        df["letter"] = df["letter"].str.replace(" ", "")

        # Update "study_ID" and "brain_side" based on the first 6 characters of the file name
        study_ID = new_filename[:6]
        df["study_ID"] = study_ID
        df["brain_side"] = study_ID[-1]

        # Update "visit" based on the presence of certain keywords in the file name
        for keyword in ["Baseline", "6mo", "12mo", "18mo", "24mo"]:
            if keyword in new_filename:
                df["visit"] = keyword
                break

        # Update "mA" based on the presence of a pattern in the file name
        mA_match = re.search(r'(\d+\.\d+)mA', new_filename)
        if mA_match:
            df["mA"] = mA_match.group(1)
        
        ordinality_match = re.search(r'(Baseline|6mo|12mo|18mo|24mo)_(\d{2})', new_filename)
        if ordinality_match:
            df["ordinality"] = ordinality_match.group(2)

        # Write the DataFrame back to the CSV file
        df.to_csv(os.path.join(directory, new_filename), index=False)