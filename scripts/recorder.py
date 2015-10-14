#!/usr/bin/env python

import os, sim, sys, time

def die(message):
    print('Error: %s.' % message)
    sys.exit(1)

studio = os.getenv('STUDIO_ROOT')
if not studio: die('STUDIO_ROOT should be defined')

toolbox = os.getenv('TOOLBOX_ROOT')
if not toolbox: die('TOOLBOX_ROOT should be defined')

program = os.getenv('PROGRAM_NAME')
if not program: die('PROGRAM_NAME should be defined')

mcpat_bin = os.path.join(studio, 'scripts', 'mcpat.py')
if not os.path.exists(mcpat_bin): die('cannot find mcpat.py')

recorder_bin = os.path.join(toolbox, 'bin', 'recorder')
if not os.path.exists(recorder_bin): die('cannot find Recorder')

output = sim.config.output_dir
period = 1e6 * sim.util.Time.NS

redis_bin = 'redis-cli'
server = '127.0.0.1:6379'
queue = 'recorder-%s' % program

sqlite_bin = 'sqlite3'
database = os.path.join(output, '%s.sqlite3' % program)
dynamic_table = 'dynamic'
static_table = 'static'

log = os.path.join(output, '%s.log' % program)
log = open(log, 'w')

class Recorder:
    def setup(self, args):
        self.start_time = time.time()
        reset()
        self.t_last = None
        recorder_dynamic_start()
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
        recorder_dynamic_stop()
        log.write('Elapsed time: %s s\n' % (time.time() - self.start_time))

    def compute_static(self, t):
        filebase = os.path.join(output, 'static')
        recorder_static_send(filebase, t)

    def compute_dynamic(self, t0, t1):
        filebase = os.path.join(output, 'dynamic-%s' % t0)
        recorder_dynamic_send(filebase, t0, t1)

def reset():
    run('%s DEL %s > /dev/null' % (redis_bin, queue))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, static_table))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, dynamic_table))

def recorder_dynamic_send(filebase, t0, t1):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
        mcpat_bin, filebase, output, t0, t1
    ))
    run('%s RPUSH %s "recorder:%.15e;%s" > /dev/null &' % (
        redis_bin, queue, float(t0) / sim.util.Time.S, filebase + '.xml'
    ))

def recorder_dynamic_start():
    run('%s dynamic --server %s --queue %s --caching --database %s --table %s &' % (
        recorder_bin, server, queue, database, dynamic_table
    ))

def recorder_dynamic_stop():
    run('%s RPUSH %s recorder:halt > /dev/null' % (redis_bin, queue))

def recorder_static_send(filebase, t):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
        mcpat_bin, filebase, output, 'start', t
    ))
    run('%s static --server %s --caching --config %s --database %s --table %s &' % (
        recorder_bin, server, filebase + '.xml', database, static_table
    ))

def report(message):
    print('-------> [%-15s] %s' % (program, message))

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

sim.util.register(Recorder())
