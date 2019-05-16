import common
import subprocess
import argparse, sys, os
from pydub import AudioSegment
from audio_augment import AudioAugmentation
import numpy as np

## run test to check how well the algorithm handles re-sapling to
## change the pitch (which also speeds up/slows down the song)
def main(args):
  dbase = args.dbase
  num_files_to_test = int(args.num_files_to_test)
  source_dir = args.source_dir
  start_timestep = int(args.start_timestep)
  sample_length = int(args.sample_length)
  pitch_range = float(args.pitch_range)
  pitch_step = float(args.pitch_step)

  aa = AudioAugmentation()
  octaves = np.linspace(-pitch_range, pitch_range, int(2*pitch_range//pitch_step))
  accuracies = [0] * len(octaves)

  numfiles = 0
  for filename in os.listdir("songs"):
    if filename[-4:] == ".mp3": 
      song = AudioSegment.from_mp3(source_dir+"/"+filename)
      sample = song[start_timestep:start_timestep+sample_length]  # take a sample from the song
      for i, octave in enumerate(octaves):
        shifted, new_sr = aa.pitch_shift(sample, octave)  # re-sample to a different octave
        shifted.export("sample.mp3", format="mp3")
        command = "python audfprint.py -h 12 -n 18 -x 1 match --dbase {} sample.mp3".format(dbase)
        result = subprocess.getoutput(command)
        match = filename in result
        print(filename, "octave:", octave, match)
        if match:
          accuracies[i] += 1
      numfiles += 1

      if numfiles == num_files_to_test:
        print(np.array(accuracies) * 100 / numfiles)
        return

if __name__ == "__main__":
  parser=argparse.ArgumentParser()

  parser.add_argument('--dbase', help='database file (with .pklz ending)')
  parser.add_argument('--num_files_to_test', help='how many files to test')
  parser.add_argument('--source_dir', help='directory where the overlay files are stored')
  parser.add_argument('--start_timestep', help='timestep to start the sample at (ms)')
  parser.add_argument('--sample_length', help='length of the sample (ms)')
  parser.add_argument('--pitch_range', help='test pitches between -pr to +pr')
  parser.add_argument('--pitch_step', help='test pitches between -pr to +pr with this step')

  args=parser.parse_args()
  main(args)
