#!/usr/bin/env python

import os, sim, sys, time

def die(message):
    print('Error: %s.' % message)
    sys.exit(1)

output = sim.config.output_dir
period = 1e6 * sim.util.Time.NS

arsenal = os.getenv('ARSENAL_ROOT')
if not arsenal: die('ARSENAL_ROOT should be defined')

benchmark = os.getenv('BENCHMARK_NAME')
if not benchmark: die('BENCHMARK_NAME should be defined')

mcpat_bin = os.path.join(arsenal, 'scripts', 'mcpat.py')
if not os.path.exists(mcpat_bin): die('cannot find mcpat.py')

squire_bin = os.path.join(arsenal, 'tools', 'bin', 'squire')
if not os.path.exists(squire_bin): die('cannot find squire')

redis_bin = 'redis-cli'
server = '127.0.0.1:6379'
queue = 'squire-%s' % benchmark

sqlite_bin = 'sqlite3'
database = os.path.join(output, '%s.sqlite3' % benchmark)
dynamic_table = 'dynamic'
static_table = 'static'

class Bullet:
    def setup(self, args):
        reset()
        self.t_last = None
        squire_dynamic_start()
        sim.util.Every(period, self.periodic, roi_only = True)

    def periodic(self, t, _):
        report('%10.2f ms' % (t / sim.util.Time.MS))
        sim.stats.write(str(t))
        if self.t_last == None:
            self.compute_static(t)
        else:
            self.compute_dynamic(self.t_last, t)
        self.t_last = t

    def hook_sim_end(self):
        squire_dynamic_stop()

    def compute_static(self, t):
        filebase = os.path.join(output, 'static')
        squire_static_send(filebase, t)

    def compute_dynamic(self, t0, t1):
        filebase = os.path.join(output, 'dynamic-%s' % t0)
        squire_dynamic_send(filebase, t0, t1)

def reset():
    run('%s DEL %s > /dev/null' % (redis_bin, queue))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, static_table))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, dynamic_table))

def squire_dynamic_send(filebase, t0, t1):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
      mcpat_bin, filebase, output, t0, t1
    ))
    run('%s RPUSH %s "squire:%.15e;%s" > /dev/null &' % (
      redis_bin, queue, float(t0) / sim.util.Time.S, filebase + '.xml'
    ))

def squire_dynamic_start():
    run('%s dynamic --server %s --queue %s --caching --database %s --table %s &' % (
        squire_bin, server, queue, database, dynamic_table
    ))

def squire_dynamic_stop():
    run('%s RPUSH %s squire:halt > /dev/null' % (redis_bin, queue))

def squire_static_send(filebase, t):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
      mcpat_bin, filebase, output, 'start', t
    ))
    run('%s static --server %s --caching --config %s --database %s --table %s &' % (
        squire_bin, server, filebase + '.xml', database, static_table
    ))

def report(message):
    print('-------> [%-15s] %s' % (benchmark, message))

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

sim.util.register(Bullet())
