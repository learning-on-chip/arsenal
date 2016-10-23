#!/usr/bin/env python

import sys

SUITE = 'parsec'

def abort():
    sys.stderr.write('Usage: configure.py {}-<benchmark name>-<input size>\n'.format(SUITE))
    sys.exit(1)

def compute_cores_threads(benchmark):
    cores, threads = int(0), int(0)
    while threads <= 0:
        cores += 1
        threads = compute_threads(benchmark, cores)
    return (cores, threads)

def compute_threads(benchmark, threads):
    if benchmark == 'blackscholes':
        threads = threads - 1
    elif benchmark == 'bodytrack':
        threads = threads - 2
    elif benchmark == 'facesim':
        threads = threads
    elif benchmark == 'ferret':
        threads = (threads - 2) / 4
    elif benchmark == 'fluidanimate':
        if threads > 1:
            threads = 1 << log2(threads - 1)
        else:
            threads = -1
    elif benchmark == 'swaptions':
        threads = threads - 1
    elif benchmark == 'canneal':
        threads = threads - 1
    elif benchmark == 'raytrace':
        threads = threads - 1
    elif benchmark == 'dedup':
        threads = threads / 4
    elif benchmark == 'streamcluster':
        threads = threads - 1
    elif benchmark == 'vips':
        threads = threads - 2
    return threads

def decompose(program):
    chunks = program.split('-')
    if len(chunks) != 3:
        abort()
    return chunks[1], chunks[2]

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
    benchmark, input = decompose(program)
    cores, threads = compute_cores_threads(benchmark)
    arguments = []
    arguments.extend(['-B', 'force_nthreads', '-n', threads])
    arguments.extend(['-g', '--general/total_cores={}'.format(cores)])
    arguments.extend(['-p', '{}-{}'.format(SUITE, benchmark), '-i', input])
    return arguments

def process_multiple(programs):
    benchmarks = []
    total_cores = 0
    for program in programs:
        benchmark, input = decompose(program)
        cores, _ = compute_cores_threads(program)
        benchmarks.append("{}-{}-{}-{}".format(SUITE, benchmark, input, cores))
        total_cores += cores
    benchmarks = ','.join(benchmarks)
    sys.stdout.write('-n {} --benchmarks={}'.format(total_cores, benchmarks))

arguments = process(sys.argv[1:])
sys.stdout.write(' '.join([str(argument) for argument in arguments]))
