import subprocess
import argparse, sys, os
from pydub import AudioSegment

## run test to check how well the algorithm recognises two songs playing 
## simultaneously (print out the returned results, one of which is Africa)
def main(args):
  dbase = args.dbase
  num_files_to_test = int(args.num_files_to_test)
  source_dir = args.source_dir
  start_timestep = int(args.start_timestep)
  sample_length = int(args.sample_length)

  numfiles = 0
  for filename in os.listdir(source_dir):
    if filename[-4:] == ".mp3":  # currently only accepts .mp3
      print(filename)
      song = AudioSegment.from_mp3(source_dir+"/"+filename)
      sample = song[start_timestep:start_timestep+sample_length]  # take a sample from the song
      sample.export("sample.mp3", format="mp3")
      command = "python audfprint.py -h 12 -n 18 -x 2 match --dbase {} sample.mp3".format(dbase)
      result = subprocess.getoutput(command)
      print(result)
      numfiles += 1
      if numfiles == num_files_to_test:
        print("finished!")
        return
    else:
      continue

if __name__ == "__main__":
  parser=argparse.ArgumentParser()

  parser.add_argument('--dbase', help='database file (with .pklz ending)')
  parser.add_argument('--num_files_to_test', help='how many files to test')
  parser.add_argument('--source_dir', help='directory where the overlay files are stored')
  parser.add_argument('--start_timestep', help='timestep to start the sample at (ms)')
  parser.add_argument('--sample_length', help='length of the sample (ms)')

  args=parser.parse_args()
  main(args)
