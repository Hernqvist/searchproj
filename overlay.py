import os
from pydub import AudioSegment
from tqdm import tqdm
import sys

def main(dir_path, audio_file):
    """
        Combines all music files in the provided directory 
        path with the provided audio file. Results are written
        to disk in individual sound files.

        :param dir_path: path to the directory with sound files
            to be overlayed
        :param audio_file: full path to the audio file with 
            which each file in the directory is combined
    """
    file_names = os.listdir(dir_path)
    file_names = [x for x in file_names if x.endswith(".mp3")]
    sound2 = AudioSegment.from_file(audio_file)
    for i, file_name in tqdm(enumerate(file_names)):
        sound1 = AudioSegment.from_file(os.path.join(dir_path, file_name))
        
        combined = sound1.overlay(sound2)

        combined.export("combined_{}.mp3".format(file_name.replace(" ", "").replace("-", "")), format='mp3')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 overlay.py <dir_path> <audio_file_path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
