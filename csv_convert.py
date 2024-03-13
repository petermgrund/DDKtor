import os
import pandas as pd
from colorama import Fore, init
init(autoreset=True)

print("Current working directory:", os.getcwd())

def convert_textgrid_to_csv(directory):
    csv_count = 0    
    output_directory = '/Users/petergrund/Documents/neurology/dysarthria_analysis/ddk_data'
    overwrite_all = None
    for filename in os.listdir(directory):
        if filename.endswith(".TextGrid"):
            with open(os.path.join(directory, filename), 'r') as f:
                lines = f.readlines()

            item1_intervals = []
            item2_intervals = []

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

            merged_intervals = merge_text_labels(item1_intervals, item2_intervals)

            df = pd.DataFrame(merged_intervals)

            df.rename(columns={'text': 'item2_text'}, inplace=True)

            # Create  'csv' subfolder if doesn't exist
            if not os.path.exists(os.path.join(directory, 'csv')):
                os.makedirs(os.path.join(directory, 'csv'))

            # Define output file path
            output_filename1 = os.path.join(directory, 'csv', os.path.splitext(filename)[0] + '.csv')
            output_filename2 = os.path.join(output_directory, os.path.splitext(filename)[0] + '.csv')

            # Create subfolder and output directory if don't exist
            if not os.path.exists(os.path.join(directory, 'csv')):
                os.makedirs(os.path.join(directory, 'csv'))
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            df.to_csv(output_filename1, index=False)
            df.to_csv(output_filename2, index=False)
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

convert_textgrid_to_csv('data/out_tg/')
csv_count = convert_textgrid_to_csv('data/out_tg/')

print(Fore.GREEN + f"{csv_count} files successfully converted from TextGrid to CSV. ")
print(Fore.WHITE +" Any existing CSV files with the same name were overwritten.")
