import os
import re

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".TextGrid"):
            new_filename = re.sub(r'_(?=[^_]*$)', '.', filename)
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed {filename} to {new_filename}")

def rename_files_cleanup(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".wav") and "_00" in filename:
            new_filename = filename.replace("_00", ".00")
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

rename_files('data/raw')
rename_files_cleanup('data/raw/')
