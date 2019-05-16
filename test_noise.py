import common
import subprocess
import argparse, sys, os
from audio_augment import AudioAugmentation
import numpy as np

## run test to check how well the algorithm handles samples of length 
## 5s, 10s and 15s with different amounts of additive noise
def main(args):
  dbase = args.dbase
  num_files_to_test = int(args.num_files_to_test)
  source_dir = args.source_dir
  start_timestep = int(args.start_timestep)
  sample_length = int(args.sample_length)
  max_power = int(args.max_power)

  aa = AudioAugmentation()

  # sigmas = [0.0, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5]
  sigmas = [0.0] + [10**x for x in range(0,max_power+1)]
  accuracies = [0] * len(sigmas)
  numfiles = 0
  for filename in os.listdir("songs"):
    if filename[-4:] == ".mp3":  # currently only accepts .mp3
      sr, sample = aa.read("songs/"+filename, start_timestep, start_timestep+sample_length) # read sample
      for j, sigma in enumerate(sigmas):
        noisy_sample = aa.add_noise(sample, sigma) # apply gaussian noise
        aa.write("sample.mp3", sr, noisy_sample)
        command = "python3 audfprint.py -h 12 -n 18 -x 1 match --dbase {} sample.mp3".format(dbase)
        result = subprocess.getoutput(command)
        match = filename in result
        print(filename, "sigma:", sigma, match)
        if match:
          accuracies[j] += 1
      numfiles += 1

    if numfiles == num_files_to_test:
      print(np.array(accuracies) / numfiles)
      return

if __name__ == "__main__":
  parser=argparse.ArgumentParser()

  parser.add_argument('--dbase', help='database file (with .pklz ending)')
  parser.add_argument('--num_files_to_test', help='how many files to test')
  parser.add_argument('--source_dir', help='directory where the overlay files are stored')
  parser.add_argument('--start_timestep', help='timestep to start the sample at (ms)')
  parser.add_argument('--sample_length', help='length of the sample (ms)')
  parser.add_argument('--max_power', help='maximum power n (10**n) of the standard deviation')

  args=parser.parse_args()
  main(args)
