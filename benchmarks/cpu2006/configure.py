#!/bin/env python

import sys

if len(sys.argv) != 2:
  sys.stderr.write('Usage: configure.py <program>\n')
  sys.exit(1)

sys.stdout.write("-n 1 -p cpu2006-%s -i large" % sys.argv[1])
