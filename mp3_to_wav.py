from pydub import AudioSegment
import os

def get_mp3_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".mp3")]

def convert_all_mp3_to_wav(input_directory, output_directory):
    all_conversions_successful = True
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(input_directory, filename)
            wav_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".wav")
            print(f"Converting {mp3_path} to {wav_path}...")
            try:
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")
                print(f"Successfully converted {mp3_path} to {wav_path}")
            except Exception as e:
                print(f"Failed to convert {mp3_path} to {wav_path}. Error: {e}")
                all_conversions_successful = False
    return all_conversions_successful
default_directory = "/Users/petergrund/Library/CloudStorage/Box-Box/ETC_Private/Assessment_Speech/"
print("Please enter the root directory containing mp3 files to convert. Press Enter to use the default directory.")
try:
    root_directory = input(f"\033[0;30mRoot directory (default: {default_directory}): \033[0m") or default_directory
except KeyboardInterrupt:
    print("\n\033[0;31mScript interrupted by user.\033[0m")
    exit(1)
    
print("Please enter a subdirectory of \033[94m" + root_directory + "\033[0m containing mp3 files to convert. Example: ETC08/ETC08_L/ETC08_L_18mo")
try:
    subdir = input("\033[0;30mSubdirectory: \033[0m")
except KeyboardInterrupt:
    print("\n\033[0;31mScript interrupted by user.\033[0m")
    exit(1)

input_directory = os.path.join(root_directory, subdir)
output_directory = "data/raw/"

try:
    mp3_files = get_mp3_files(input_directory)
    print(f"\033[0;33mYou are about to convert {len(mp3_files)} MP3 files to WAV. Do you want to continue? (y/n) Print\033[0m list\033[0;33m to see which files you will convert.\033[0m")
    confirm = input()
    if confirm.lower() == 'list':
        print("\033[0;33mThe following files will be converted:\033[0m")
        for file in mp3_files:
            print(file)
        print(f"\033[0;33mDo you want to continue? (y/n)\033[0m")
        confirm = input()
    if confirm.lower() != 'y':
        print("\033[0;31mAborted by user.\033[0m")
        exit(0)
    all_conv_success = convert_all_mp3_to_wav(input_directory, output_directory)
except FileNotFoundError:
    print("\033[0;31mThe specified directory does not exist.\033[0m")
    exit(1)

if all_conv_success:
    print("\033[0;32mAll conversions are complete.\033[0m")
else:
    print("\033[0;31mAt least one conversion failed. Make sure your input and output directories exist.\033[0m")