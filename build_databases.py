import subprocess
import common

subprocess.call("rm -r databases", shell=True)
subprocess.call("mkdir databases", shell=True)

for bits in common.BIT_RANGE:
  for density in common.DENSITY_RANGE:
    command = "python audfprint.py -h {} -n {} new --dbase {} songs/*.mp3".format(
        bits, density, common.dbasename(bits, density))
    print(command)
    subprocess.call(command, shell=True)