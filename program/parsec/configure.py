#!/usr/bin/env python

import sys

SUITE = 'parsec'

def abort():
    sys.stderr.write('Usage: configure.py <program name>-<program input>\n')
    sys.exit(1)

def compute_cores_threads(name):
    cores, threads = int(0), int(0)
    while threads <= 0:
        cores += 1
        threads = compute_threads(name, cores)
    return (cores, threads)

def compute_threads(name, threads):
    if name == 'blackscholes':
        threads = threads - 1
    elif name == 'bodytrack':
        threads = threads - 2
    elif name == 'facesim':
        threads = threads
    elif name == 'ferret':
        threads = (threads - 2) / 4
    elif name == 'fluidanimate':
        if threads > 1:
            threads = 1 << log2(threads - 1)
        else:
            threads = -1
    elif name == 'swaptions':
        threads = threads - 1
    elif name == 'canneal':
        threads = threads - 1
    elif name == 'raytrace':
        threads = threads - 1
    elif name == 'dedup':
        threads = threads / 4
    elif name == 'streamcluster':
        threads = threads - 1
    elif name == 'vips':
        threads = threads - 2
    return threads

def decompose(program):
    chunks = program.split('-')
    if len(chunks) != 2:
        abort()
    return chunks[0], chunks[1]

def log2(n):
    result = -1
    while n:
        n >>= 1
        result += 1
    return result

def process(programs):
    if len(programs) == 0:
        abort()
    if len(programs) == 1:
        return process_single(programs[0])
    else:
        return process_multiple(programs)

def process_single(program):
    name, input = decompose(program)
    cores, threads = compute_cores_threads(name)
    arguments = []
    arguments.extend(['-B', 'force_nthreads', '-n', threads])
    arguments.extend(['-g', '--general/total_cores={}'.format(cores)])
    arguments.extend(['-p', '{}-{}'.format(SUITE, name), '-i', input])
    return arguments

def process_multiple(programs):
    benchmarks = []
    total_cores = 0
    for program in programs:
        name, input = decompose(program)
        cores, _ = compute_cores_threads(program)
        benchmarks.append("{}-{}-{}-{}".format(SUITE, program, input, cores))
        total_cores += cores
    benchmarks = ','.join(benchmarks)
    sys.stdout.write('-n {} --benchmarks={}'.format(total_cores, benchmarks))

arguments = process(sys.argv[1:])
sys.stdout.write(' '.join([str(argument) for argument in arguments]))
