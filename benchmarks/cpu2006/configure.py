#!/bin/env python

import sys

def process_single(program):
  sys.stdout.write("-n 1 -p cpu2006-%s -i large" % sys.argv[1])

def process_multiple(programs):
  benchmarks = []
  total_ncores = 0
  for program in programs:
    ncores = 1
    benchmarks.append("cpu2006-%s-large-%d" % (program, ncores))
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
