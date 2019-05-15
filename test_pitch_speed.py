import common
import subprocess
import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from audio_augment import AudioAugmentation
import numpy as np
import audio_read

## run test to check how well the algorithm handles re-sapling to
## change the pitch (which also speeds up/slows down the song)
bits = 12
density = 18
num_files_to_test = 25
aa = AudioAugmentation()
octaves = [-0.1, -0.05, -0.01, -0.005, -0.001, 0.0, 0.001, 0.005, 0.01, 0.05, 0.1]
accuracies = [0] * len(octaves)

numfiles = 0
for filename in os.listdir("songs"):
  if (filename == ".DS_Store") or (filename == ".DSStore"):
    continue
  song = AudioSegment.from_mp3("songs/"+filename)
  sample = song[40000:55000]  # take a sample from the song
  for i, octave in enumerate(octaves):
    shifted, new_sr = aa.pitch_shift(sample, octave)  # re-sample to a different octave
    # print("old duration: {:.2f}s, new duration: {:.2f}s, proportion: {:.3f}".format(
      # sample.duration_seconds, shifted.duration_seconds, shifted.duration_seconds/sample.duration_seconds))
    shifted.export("sample.mp3".format(octave), format="mp3")
    command = "python audfprint.py -h {} -n {} -x 1 match --dbase {} sample.mp3".format(
            bits, density, common.dbasename(bits, density))
    result = subprocess.getoutput(command)
    match = filename in result
    print(filename, "octave:", octave, match)
    if match:
      accuracies[i] += 1
  
  numfiles += 1

  if numfiles == num_files_to_test:
    break

print(np.array(accuracies) * 100 / num_files_to_test)