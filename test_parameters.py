import common
import subprocess
import argparse, sys, os
from pydub import AudioSegment

## run grid search to find the optimal parameter values for the number of bits
## in each hash and the density of hashes per second
def main(args):
  dbase_dir = args.dbase_dir
  num_files_to_test = int(args.num_files_to_test)
  source_dir = args.source_dir
  start_timestep = int(args.start_timestep)
  sample_length = int(args.sample_length)

  correct = [[0 for density in common.DENSITY_RANGE] for bits in common.BIT_RANGE]
  
  numfiles = 0
  for filename in os.listdir(source_dir):
    if filename[-4:] == ".mp3":  # currently only accepts .mp3
      song = AudioSegment.from_mp3(source_dir+"/"+filename)
      sample = song[start_timestep:start_timestep+sample_length]  # take a sample from the song
      sample.export("sample.mp3", format="mp3")
      for i, bits in enumerate(common.BIT_RANGE):
        for j, density in enumerate(common.DENSITY_RANGE):
          command = "python audfprint.py -h {} -n {} -x 1 match --dbase {} sample.mp3".format(
            bits, density, "{}/b{}_d{}.pklz".format(dbase_dir, bits, density))
          result = subprocess.getoutput(command)
          match = filename in result
          print(filename, bits, "bits,", density, "density", match)
          if match:
            correct[i][j] += 1
      numfiles += 1
      if numfiles == num_files_to_test:
        # print out the grid with accuracies
        print("\t"+"".join(["d:{}\t".format(d) for d in common.DENSITY_RANGE]))
        for i, bits in enumerate(common.BIT_RANGE):
          print("b:{}\t".format(bits) + 
            "".join("{:.2f}\t".format(c*100/numfiles) for c in correct[i]))
        return

if __name__ == "__main__":
  parser=argparse.ArgumentParser()

  parser.add_argument('--dbase_dir', help='directory where databases are stored')
  parser.add_argument('--num_files_to_test', help='how many files to test')
  parser.add_argument('--source_dir', help='directory where the overlay files are stored')
  parser.add_argument('--start_timestep', help='timestep to start the sample at (ms)')
  parser.add_argument('--sample_length', help='length of the sample (ms)')

  args=parser.parse_args()
  main(args)
