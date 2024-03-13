import os

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".wav") and '.' in filename.split('_')[-2]:
            new_filename = filename.replace('.', '_')
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed {filename} to {new_filename}")

def check_matching_files(directory):
    wav_files = set(file for file in os.listdir(directory) if file.endswith('.wav'))
    textgrid_files = set(file for file in os.listdir(directory) if file.endswith('.TextGrid'))

    wav_names = set(name[:-4] for name in wav_files)  # Remove extension
    textgrid_names = set(name[:-9] for name in textgrid_files)  # Remove extension

    matching_files = wav_names & textgrid_names  # Intersection of two sets
    print(f'Total number of matches: {len(matching_files)}')

    wav_without_match = wav_names - textgrid_names
    textgrid_without_match = textgrid_names - wav_names

    if wav_without_match:
        print('WAV files without a matching TextGrid file:')
        for name in wav_without_match:
            print(name + '.wav')

    if textgrid_without_match:
        print('TextGrid files without a matching WAV file:')
        for name in textgrid_without_match:
            print(name + '.TextGrid')

directory = input('Enter the directory to check: ')
rename_files(directory)
check_matching_files(directory)