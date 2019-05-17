from audio_augment import AudioAugmentation
from pydub import AudioSegment
import sys

def produce_shifted_music(file_name, shift_in_octaves):
    song = AudioSegment.from_mp3(file_name)
    aa = AudioAugmentation()
    shifted, new_sr = aa.pitch_shift(song, shift_in_octaves)
    shifted.export("pitch_output_{}.mp3".format(shift_in_octaves), format="mp3")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 audio_pitch_creator.py <music_file_name> <shift_in_octaves>")
    produce_shifted_music(sys.argv[1], float(sys.argv[2]))
