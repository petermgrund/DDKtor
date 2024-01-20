from pydub import AudioSegment
import os

def convert_all_mp3_to_wav(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(directory, filename)
            wav_path = os.path.join(directory, os.path.splitext(filename)[0] + ".wav")
            print(f"Converting {mp3_path} to {wav_path}...")
            try:
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")
                print(f"Successfully converted {mp3_path} to {wav_path}")
            except Exception as e:
                print(f"Failed to convert {mp3_path} to {wav_path}. Error: {e}")

convert_all_mp3_to_wav("data/raw/")
print("\033[0;32mAll conversions are complete.\033[0m")