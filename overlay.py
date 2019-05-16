import os
from pydub import AudioSegment
from tqdm import tqdm

def main(dir_path):
    file_names = os.listdir(dir_path)
    file_names = [x for x in file_names if x.endswith(".mp3")]
    sound2 = AudioSegment.from_file("../songs/Toto - Africa (Official Music Video).mp3")
    for i, file_name in tqdm(enumerate(file_names)):
        sound1 = AudioSegment.from_file(os.path.join(dir_path, file_name))
        
        combined = sound1.overlay(sound2)

        combined.export("combined_{}.mp3".format(file_name.replace(" ", "").replace("-", "")), format='mp3')

if __name__ == "__main__":
    main("../songs")