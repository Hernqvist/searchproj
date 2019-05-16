import common
import subprocess
import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from pydub.effects import speedup
from audio_augment import AudioAugmentation
import numpy as np
import audio_read

## run test to check how well the algorithm handles re-sapling to
## change the pitch (which also speeds up/slows down the song)
bits = 12
density = 18
num_files_to_test = 50
aa = AudioAugmentation()
two_matches = 0
only_africa = 0
only_other = 0
no_matches = 0

numfiles = 0
for filename in os.listdir("combined"):
  if (filename == ".DS_Store") or (filename == ".DSStore"):
    continue

  temp = filename.split("_")[1]
  print(temp)
  song = AudioSegment.from_mp3("combined/"+filename)
  sample = song[60000:75000]  # take a sample from the song
  sample.export("sample.mp3", format="mp3")
  command = "python audfprint.py -h {} -n {} -x 2 match --dbase {} sample.mp3".format(
        bits, density, common.dbasename(bits, density))
  result = subprocess.getoutput(command)
  print(result)
  if ("Toto - Africa" in result) and (temp[:4] in result):
    print("TWO MATCHES")
    two_matches += 1
  elif ("Toto - Africa" in result):
    only_africa += 1
    print("AFRICA")
  elif (temp[:4] in result):
    only_other += 1
    print("OTHER")
  else:
    print("NO MATCHES")
    no_matches += 1

  print(two_matches, only_africa, only_other, no_matches)
  numfiles += 1
  # except:
    # print("Something went wrong with file {}, skipping.".format(filename))

  if numfiles == num_files_to_test:
    break