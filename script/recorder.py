#!/usr/bin/env python

import os, sim, sys, time

class Config:
    def __init__(self):
        self.studio = os.getenv('STUDIO_ROOT')
        if not self.studio: die('STUDIO_ROOT should be defined')

        self.toolbox = os.getenv('TOOLBOX_ROOT')
        if not self.toolbox: die('TOOLBOX_ROOT should be defined')

        self.program = os.getenv('PROGRAM_NAME')
        if not self.program: die('PROGRAM_NAME should be defined')

        self.output = sim.config.output_dir
        self.period = 1e6 * sim.util.Time.NS

        self.redis = {
            'bin': 'redis-cli',
            'server': '127.0.0.1:6379',
            'queue': 'recorder-%s' % self.program,
        }

        self.sqlite = {
            'bin': 'sqlite3',
            'database': os.path.join(self.output, '%s.sqlite3' % self.program),
            'dynamic': 'dynamic',
            'static': 'static',
        }

class Worker:
    def __init__(self, config):
        self.program = config.program
        self.output = config.output
        self.redis = config.redis
        self.sqlite = config.sqlite

        self.recorder = os.path.join(config.toolbox, 'bin', 'recorder')
        if not os.path.exists(self.recorder): die('cannot find Recorder')

        self.mcpat = os.path.join(config.studio, 'script', 'mcpat.py')
        if not os.path.exists(self.mcpat): die('cannot find mcpat.py')

    def start_dynamic(self):
        run('%s dynamic --server %s --queue %s --caching --database %s --table %s &' % (
            self.recorder, self.redis['server'], self.redis['queue'],
            self.sqlite['database'], self.sqlite['dynamic']
        ))

    def stop_dynamic(self):
        run('%s RPUSH %s recorder:halt > /dev/null' % (
            self.redis['bin'], self.redis['queue'])
        )

    def process_dynamic(self, t0, t1):
        self.progress('%10.2f ms' % (t1 / sim.util.Time.MS))
        filebase = os.path.join(self.output, 'dynamic-%s' % t0)
        run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
            self.mcpat, filebase, self.output, t0, t1
        ))
        run('%s RPUSH %s "recorder:%.15e;%s" > /dev/null &' % (
            self.redis['bin'], self.redis['queue'], float(t0) / sim.util.Time.S,
            filebase + '.xml'
        ))

    def process_static(self, t):
        filebase = os.path.join(self.output, 'static')
        run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
            self.mcpat, filebase, self.output, 'start', t
        ))
        run('%s static --server %s --caching --config %s --database %s --table %s &' % (
            self.recorder, self.redis['server'], filebase + '.xml',
            self.sqlite['database'], self.sqlite['static']
        ))

    def reset(self):
        run('%s DEL %s > /dev/null' % (self.redis['bin'], self.redis['queue']))
        run('%s %s "DROP TABLE IF EXISTS %s;"' % (
            self.sqlite['bin'], self.sqlite['database'], self.sqlite['static'])
        )
        run('%s %s "DROP TABLE IF EXISTS %s;"' % (
            self.sqlite['bin'], self.sqlite['database'], self.sqlite['dynamic'])
        )

    def progress(self, message):
        print('-------> [%-15s] %s' % (self.program, message))

class Listener:
    def __init__(self, worker, config):
        self.worker = worker
        self.period = config.period

        filename = os.path.join(config.output, '%s.log' % config.program)
        self.logger = open(filename, 'w')

    def setup(self, _):
        self.t_start = time.time()
        self.t_last = None
        self.worker.start_dynamic()
        sim.util.Every(self.period, self.periodic, roi_only=True)

    def periodic(self, t, _):
        sim.stats.write(str(t))
        if self.t_last == None: self.worker.process_static(t)
        else: self.worker.process_dynamic(self.t_last, t)
        self.t_last = t

    def hook_sim_end(self):
        self.worker.stop_dynamic()
        self.logger.write('Elapsed time: %s s\n' % (time.time() - self.t_start))

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

def die(message):
    raise SystemError(message)

config = Config()

worker = Worker(config)
worker.reset()

listener = Listener(worker, config)

sim.util.register(listener)
