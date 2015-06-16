import os, sim, sys, time

def die(message):
    print('Error: %s.' % message)
    sys.exit(1)

output = sim.config.output_dir
period = 1e6 * sim.util.Time.NS

benchmark = os.getenv('BENCHMARK_NAME')
if not benchmark: die('cannot identify the benchmark')

mcpat_bin = os.path.join(os.getenv('TOOLS_ROOT'), 'mcpat.py')
if not os.path.exists(mcpat_bin): die('cannot find mcpat.py')

squire_bin = os.path.join(os.getenv('SQUIRE_ROOT'), 'bin', 'squite')
if not os.path.exists(squite_bin): die('cannot find squite')

results = os.getenv('RESULTS_ROOT')
if not results: die('cannot idenitfy the results directory')

redis_bin = 'redis-cli'
server = '127.0.0.1:6379'
queue = 'squite-%s' % benchmark

sqlite_bin = 'sqlite3'
database = os.path.join(results, '%s.sqlite3' % benchmark)
dynamic_table = 'dynamic'
static_table = 'static'

class Bullet:
    def setup(self, args):
        reset()
        self.t_last = None
        squite_dynamic_start()
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
        squite_dynamic_stop()

    def compute_static(self, t):
        filebase = os.path.join(output, 'static')
        squite_static_send(filebase, t)

    def compute_dynamic(self, t0, t1):
        filebase = os.path.join(output, 'dynamic-%s' % t0)
        squite_dynamic_send(filebase, t0, t1)

def reset():
    run('%s DEL %s > /dev/null' % (redis_bin, queue))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, static_table))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, dynamic_table))

def squite_dynamic_send(filebase, t0, t1):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
      mcpat_bin, filebase, output, t0, t1
    ))
    run('%s RPUSH %s "squite:%.15e;%s" > /dev/null &' % (
      redis_bin, queue, float(t0) / sim.util.Time.S, filebase + '.xml'
    ))

def squite_dynamic_start():
    run('%s dynamic --server %s --queue %s --caching --database %s --table %s &' % (
        squite_bin, server, queue, database, dynamic_table
    ))

def squite_dynamic_stop():
    run('%s RPUSH %s squite:halt > /dev/null' % (redis_bin, queue))

def squite_static_send(filebase, t):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
      mcpat_bin, filebase, output, 'start', t
    ))
    run('%s static --server %s --caching --config %s --database %s --table %s &' % (
        squite_bin, server, filebase + '.xml', database, static_table
    ))

def report(message):
    print('-------> [%-15s] %s' % (benchmark, message))

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

sim.util.register(Bullet())
