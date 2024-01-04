import os
import pandas as pd
from colorama import Fore, init
init(autoreset=True)

def convert_textgrid_to_csv(directory):
    csv_count = 0    
    for filename in os.listdir(directory):
        if filename.endswith(".TextGrid"):
            # Read the TextGrid file
            with open(os.path.join(directory, filename), 'r') as f:
                lines = f.readlines()

            # Initialize empty lists to store the intervals for item 1 and item 2
            item1_intervals = []
            item2_intervals = []

            # Loop over the lines in the file to extract the intervals for item 1 and item 2
            for i in range(len(lines)):
                if 'item [1]' in lines[i]:
                    j = i + 1
                    while 'item [2]' not in lines[j]:
                        if 'xmin' in lines[j] and 'xmax' in lines[j+1] and 'text' in lines[j+2]:
                            xmin = float(lines[j].split('=')[1].strip())
                            xmax = float(lines[j+1].split('=')[1].strip())
                            text = lines[j+2].split('=')[1].strip().strip('""')
                            item1_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
                        j += 1
                elif 'item [2]' in lines[i]:
                    j = i + 1
                    while j < len(lines) and 'item [' not in lines[j]:
                        if 'xmin' in lines[j] and 'xmax' in lines[j+1] and 'text' in lines[j+2]:
                            xmin = float(lines[j].split('=')[1].strip())
                            xmax = float(lines[j+1].split('=')[1].strip())
                            text = lines[j+2].split('=')[1].strip().strip('""')
                            item2_intervals.append({'xmin': xmin, 'xmax': xmax, 'text': text})
                        j += 1

            # Merge the text labels from item 1 onto the intervals from item 2
            merged_intervals = merge_text_labels(item1_intervals, item2_intervals)

            # Convert the list of merged intervals to a DataFrame
            df = pd.DataFrame(merged_intervals)

            # Rename the 'text' column to 'item2_text'
            df.rename(columns={'text': 'item2_text'}, inplace=True)

            # Write the DataFrame to a CSV file
            # Create the 'csv' subfolder if it doesn't exist
            if not os.path.exists(os.path.join(directory, 'csv')):
                os.makedirs(os.path.join(directory, 'csv'))

            # Define the output file path, including the 'csv' subfolder
            output_filename = os.path.join(directory, 'csv', os.path.splitext(filename)[0] + '.csv')

            # Write the DataFrame to a CSV file in the 'csv' subfolder
            df.to_csv(output_filename, index=False)
            csv_count += 1
    return csv_count

def merge_text_labels(item1_intervals, item2_intervals):
    merged_intervals = []

    for i, interval2 in enumerate(item2_intervals):
        overlapping_intervals = [interval1 for interval1 in item1_intervals if interval1['xmax'] > interval2['xmin'] and interval1['xmin'] < interval2['xmax']]

        if overlapping_intervals:
            # Only merge the text values if there is exactly one overlapping interval from item 1 and its text is not blank
            if len(overlapping_intervals) == 1 and overlapping_intervals[0]['text'].strip() != '':
                interval2['item1_text'] = overlapping_intervals[0]['text']
            else:
                interval2['item1_text'] = ''
        else:
            interval2['item1_text'] = ''

        # If this is the last interval, set item1_text to an empty string
        if i == len(item2_intervals) - 1:
            interval2['item1_text'] = ''

        merged_intervals.append(interval2)

    return merged_intervals

# Call the functions
convert_textgrid_to_csv('data/out_tg/')
csv_count = convert_textgrid_to_csv('data/out_tg/')

print(Fore.GREEN + f"{csv_count} files successfully converted from TextGrid to CSV.")