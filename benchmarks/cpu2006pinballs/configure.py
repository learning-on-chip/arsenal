#!/bin/env python

import os, sys

if len(sys.argv) != 2:
  sys.stderr.write('Usage: configure.py <program>\n')
  sys.exit(1)

pinballs = os.getenv('PINBALLS_ROOT')
if not pinballs:
  print('PINBALLS_ROOT should be defined')
  sys.exit(1)

sys.stdout.write("--pinballs=%s/cpu2006-%s/pinball" % (pinballs, sys.argv[1]))
