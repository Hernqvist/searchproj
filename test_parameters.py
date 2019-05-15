import common
import subprocess
import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

## run grid search to find the optimal parameter values for the number of bits
## in each hash and the density of hashes per second
num_files_to_test = 25

correct = [[0 for density in common.DENSITY_RANGE] for bits in common.BIT_RANGE]
numfiles = 0
for filename in os.listdir("songs"):
  if (filename == ".DS_Store") or (filename == ".DSStore"):
    continue
  numfiles += 1
  try:
    song = AudioSegment.from_mp3("songs/"+filename)
  except CouldntDecodeError:
    print("Failed to decode " + filename + " as an audio file, skipped")
    continue
  sample = song[:20000][-5000:]  # take a sample from the song
  sample.export("sample.mp3", format="mp3")
  for i, bits in enumerate(common.BIT_RANGE):
    for j, density in enumerate(common.DENSITY_RANGE):
      command = "python audfprint.py -h {} -n {} -x 1 match --dbase {} sample.mp3".format(
        bits, density, common.dbasename(bits, density))
      result = subprocess.getoutput(command)
      match = filename in result
      print(filename, bits, "bits,", density, "density", match)
      if match:
        correct[i][j] += 1
  if numfiles == num_files_to_test:
    break

# print out the grid with accuracies
print("\t"+"".join(["d:{}\t".format(d) for d in common.DENSITY_RANGE]))
for i, bits in enumerate(common.BIT_RANGE):
  print("b:{}\t".format(bits) + 
    "".join("{:.2f}\t".format(c/numfiles) for c in correct[i]))