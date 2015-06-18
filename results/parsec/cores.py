#!/bin/env python

import sys

def log2(n):
  log2n = -1
  while n:
      n >>= 1
      log2n += 1
  return log2n

def get_nthreads(program, nthreads):
  if program == 'blackscholes':
    nthreads = nthreads - 1
  elif program == 'bodytrack':
    nthreads = nthreads - 2
  elif program == 'facesim':
    nthreads = nthreads
  elif program == 'ferret':
    nthreads = (nthreads - 2) / 4
  elif program == 'fluidanimate':
    if nthreads > 1: nthreads = 1 << log2(nthreads - 1)
    else: nthreads = -1
  elif program == 'swaptions':
    nthreads = nthreads - 1
  elif program == 'canneal':
    nthreads = nthreads - 1
  elif program == 'raytrace':
    nthreads = nthreads - 1
  elif program == 'dedup':
    nthreads = nthreads / 4
  elif program == 'streamcluster':
    nthreads = nthreads - 1
  elif program == 'vips':
    nthreads = nthreads - 2
  else:
    nthreads = nthreads

  return nthreads

if len(sys.argv) != 2:
  sys.stderr.write('Usage: cores.py <program>\n')
  sys.exit(1)

program = sys.argv[1]

cores = int(1)
while get_nthreads(program, cores) <= 0:
  cores += 1

sys.stdout.write(str(cores))
