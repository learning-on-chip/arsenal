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

bullet_bin = os.path.join(os.getenv('BULLET_ROOT'), 'bin', 'bullet')
if not os.path.exists(bullet_bin): die('cannot find bullet')

results = os.getenv('RESULTS_ROOT')
if not results: die('cannot idenitfy the results directory')

redis_bin = 'redis-cli'
server = '127.0.0.1:6379'
queue = 'bullet-%s' % benchmark

sqlite_bin = 'sqlite3'
database = os.path.join(results, '%s.sqlite3' % benchmark)
area_table = 'area'
power_table = 'power'

class Bullet:
    def setup(self, args):
        reset()
        self.t_last = None
        bullet_power_start()
        sim.util.Every(period, self.periodic, roi_only = True)

    def periodic(self, t, _):
        report('%.2f ms' % (t / sim.util.Time.MS))
        t = coarse(t)
        sim.stats.write(str(t))
        if self.t_last == None:
            self.compute_area(t)
        else:
            self.compute_power(self.t_last, t)
        self.t_last = t

    def hook_sim_end(self):
        bullet_power_stop()

    def compute_area(self, t):
        filebase = os.path.join(output, 'area')
        bullet_area_send(filebase, t)

    def compute_power(self, t0, t1):
        filebase = os.path.join(output, 'power-%s-%s' % (t0, t1))
        bullet_power_send(filebase, t0, t1)

def reset():
    run('%s DEL %s > /dev/null' % (redis_bin, queue))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, area_table))
    run('%s %s "DROP TABLE IF EXISTS %s;"' % (sqlite_bin, database, power_table))

def coarse(time):
    return long(long(time) / sim.util.Time.NS)

def bullet_area_send(filebase, t):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
      mcpat_bin, filebase, output, 'start', t
    ))
    run('%s area --server %s --caching --config %s --database %s --table %s &' % (
        bullet_bin, server, filebase + '.xml', database, area_table
    ))

def bullet_power_send(filebase, t0, t1):
    run('unset PYTHONHOME && %s -o %s -d %s --partial=%s:%s' % (
      mcpat_bin, filebase, output, t0, t1
    ))
    run('%s RPUSH %s %s > /dev/null &' % (
      redis_bin, queue, filebase + '.xml'
    ))

def bullet_power_start():
    run('%s power --server %s --queue %s --caching --database %s --table %s &' % (
        bullet_bin, server, queue, database, power_table
    ))

def bullet_power_stop():
    run('%s RPUSH %s bullet:halt > /dev/null' % (redis_bin, queue))

def report(message):
    print('-------> [%-15s] %s' % (benchmark, message))

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

sim.util.register(Bullet())
