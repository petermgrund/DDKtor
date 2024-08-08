import os
from pydub import AudioSegment

def convert_m4a_to_mp3(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".m4a"):
            m4a_path = os.path.join(directory, filename)
            mp3_path = os.path.join(directory, os.path.splitext(filename)[0] + ".mp3")
            print(f"Converting {filename} to {mp3_path}...")
            try:
                audio = AudioSegment.from_file(m4a_path, format="m4a")
                audio.export(mp3_path, format="mp3")
                print(f"Successfully converted {filename} to .mp3 format")
            except Exception as e:
                print(f"Failed to convert {m4a_path} to {mp3_path}. Error: {e}")

user_input = input("Please enter the directory path: ")
directory = os.path.join("../../Patients", user_input)
convert_m4a_to_mp3(directory)