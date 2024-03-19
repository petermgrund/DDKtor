from pydub import AudioSegment
import os
import shutil

def get_mp3_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".mp3")]

def get_textgrid_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.TextGrid')]

def copy_textgrid_files(input_directory, output_directory):
    count = 0
    for file in os.listdir(input_directory):
        if file.endswith(".TextGrid"):
            shutil.copy(os.path.join(input_directory, file), output_directory)
            count += 1
    return count

def convert_all_mp3_to_wav(input_directory, output_directory):
    all_conversions_successful = True
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(input_directory, filename)
            wav_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".wav")
            print(f"Converting {filename} to {wav_path}...")
            try:
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")
                print(f"Successfully converted {filename} to .wav format")
            except Exception as e:
                print(f"Failed to convert {mp3_path} to {wav_path}. Error: {e}")
                all_conversions_successful = False
    return all_conversions_successful
default_directory = "../../Data/"
print("Please enter the root directory containing mp3 files to convert. Press Enter to use the default directory.")

try:
    root_directory = input(f"\033[0;30mRoot directory (default: {default_directory}): \033[0m") or default_directory
except KeyboardInterrupt:
    print("\n\033[0;31mScript interrupted by user.\033[0m")
    exit(1)
    
print("Please enter a subdirectory or multiple subdirectories (separated by commas) of \033[94m" + default_directory + "\033[0m containing mp3 files to convert. Example: ETC08/ETC08_L/ETC08_L_18mo,ETC09/ETC09_L/ETC09_L_18mo")
try:
    subdir_input = input("\033[0;30mSubdirectory: \033[0m")
    if ',' in subdir_input:
        subdirs = subdir_input.split(',')
    else:
        subdirs = [subdir_input]
except KeyboardInterrupt:
    print("\n\033[0;31mScript interrupted by user.\033[0m")
    exit(1)

for subdir in subdirs:
    subdir = subdir.strip()
    input_directory = os.path.join(root_directory, subdir)

    etc_dir = subdir.split('/')[0]
    if not etc_dir.startswith('ETC'):
        print("\033[0;31mCould not extract ETCXX from subdirectory. Please check your input.\033[0m")
        continue  # Skip to the next directory
    output_directory = "data/raw"

    try:
        mp3_files = get_mp3_files(input_directory)
        textgrid_files = get_textgrid_files(input_directory)
        # ...

        all_conv_success = convert_all_mp3_to_wav(input_directory, output_directory)
    except FileNotFoundError:
        print("\033[0;31mThe specified directory does not exist.\033[0m")
        continue  # Skip to the next directory

    if all_conv_success:
        print("\033[0;32mAll conversions are complete and have been saved to DDKTor.\033[0m")
    else:
        print("\033[0;31mAt least one conversion failed. Make sure your input and output directories exist.\033[0m")

    textgrid_count = copy_textgrid_files(input_directory, output_directory)
    print(f"\033[0;33m{textgrid_count} TextGrid files have also been transferred to DDKTor.\033[0m")