import common
import subprocess
import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from audio_augment import AudioAugmentation
import numpy as np

num_files_to_test = 25
bits = 12
density = 18
sample_lengths = [5000, 10000, 15000]
sigmas = [0.0, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5]

for sample_length in sample_lengths:
  print("testing samples of length {} seconds".format(sample_length / 1000))
  accuracies = [0] * len(sigmas)
  start_index = 60000
  end_index = start_index + sample_length

  aa = AudioAugmentation()

  numfiles = 0
  for filename in os.listdir("songs"):
    if (filename == ".DS_Store") or (filename == ".DSStore"):
      continue
    
    try:
      sr, sample = aa.read("songs/"+filename, start_index, end_index)
      # print(np.min(sample), np.max(sample))
      for j, sigma in enumerate(sigmas):
        noisy_sample = aa.add_noise(sample, sigma)
        # print("MSE", np.mean(np.sqrt((sample - noisy_sample)**2)))
        aa.write("sample.mp3", sr, noisy_sample)
        command = "python3 audfprint.py -h {} -n {} -x 1 match --dbase {} sample.mp3".format(
          bits, density, common.dbasename(bits, density))
        result = subprocess.getoutput(command)
        match = filename in result
        print(filename, "sigma:", sigma, match)
        if match:
          accuracies[j] += 1
      numfiles += 1
    except:
      print("something went wrong with file {}, skipped".format(filename))
      continue

    if numfiles == num_files_to_test:
      break

  print(np.array(accuracies) / num_files_to_test)
