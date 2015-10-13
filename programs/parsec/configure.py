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

def find_ncores_nthreads(program):
  ncores = int(0)
  nthreads = int(0)
  while nthreads <= 0:
    ncores += 1
    nthreads = get_nthreads(program, ncores)
  return (ncores, nthreads)

def process_single(program):
  ncores, nthreads = find_ncores_nthreads(program)
  sys.stdout.write(
    "-B force_nthreads -n %d -g --general/total_cores=%d -p parsec-%s -i small" % (
      nthreads, ncores, program
    )
  )

def process_multiple(programs):
  benchmarks = []
  total_ncores = 0
  for program in programs:
    ncores, _ = find_ncores_nthreads(program)
    benchmarks.append("parsec-%s-small-%d" % (program, ncores))
    total_ncores += ncores

  sys.stdout.write(
    "-n %d --benchmarks=%s" % (total_ncores, ",".join(benchmarks))
  )

if len(sys.argv) != 2:
  sys.stderr.write('Usage: configure.py <program>\n')
  sys.exit(1)

programs = sys.argv[1].split('_')

if len(programs) == 1:
  process_single(programs[0])
else:
  process_multiple(programs)
