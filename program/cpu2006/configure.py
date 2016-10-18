#!/usr/bin/env python

import sys

SUITE = 'cpu2006'

def abort():
    sys.stderr.write('Usage: configure.py <program name>-<program input>\n')
    sys.exit(1)

def decompose(program):
    chunks = program.split('-')
    if len(chunks) != 2:
        abort()
    return chunks[0], chunks[1]

def process(programs):
    if len(programs) == 0:
        abort()
    if len(programs) == 1:
        return process_single(programs[0])
    else:
        return process_multiple(programs)

def process_single(program):
    name, input = decompose(program)
    return ['-n', 1, '-p', '{}-{}'.format(SUITE, name), '-i', input]

def process_multiple(programs):
    benchmarks = []
    total_cores = 0
    for program in programs:
        cores = 1
        name, input = decompose(program)
        benchmarks.append('{}-{}-{}-{}'.format(SUITE, program, input, cores))
        total_cores += cores
    benchmarks = ','.join(benchmarks)
    return ['-n', total_cores, '--benchmarks={}'.format(benchmarks)]

arguments = process(sys.argv[1:])
sys.stdout.write(' '.join([str(argument) for argument in arguments]))
