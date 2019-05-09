BIT_RANGE = range(2, 21, 2)
DENSITY_RANGE = range(2, 21, 2)

def dbasename(bits, density):
  return "databases/b{}_d{}.pklz".format(bits, density)