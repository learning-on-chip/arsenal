#!/bin/env python

import sys

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
    nthreads = 1 << log2(nthreads - 1)
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
  exit(1)

program = sys.argv[1]

cores = int(1)
while get_nthreads(program, cores) <= 0:
  cores += 1

sys.stdout.write(str(cores))
