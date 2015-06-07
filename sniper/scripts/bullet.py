import os, sim, sys, time

output = sim.config.output_dir
period = 1e6 * sim.util.Time.NS

mcpat_bin = os.path.join(os.getenv('TOOLS_ROOT'), 'mcpat.py')
if not os.path.exists(mcpat_bin): die('cannot find mcpat.py')

bullet_bin = os.path.join(os.getenv('BULLET_ROOT'), 'bin', 'bullet')
if not os.path.exists(bullet_bin): die('cannot find bullet')

redis_bin = 'redis-cli'

server = '127.0.0.1:6379'
queue = 'bullet-queue'
database = os.path.join(output, 'database.sqlite3')

class Bullet:
    def setup(self, args):
        bullet_start()
        self.t_last = 0
        sim.util.Every(period, self.periodic, roi_only = True)

    def periodic(self, time, elapsed):
        report('Time %.2f ms, elapsed %.2f ms' % (
            time / sim.util.Time.MS, elapsed / sim.util.Time.MS
        ))
        self.process(time)

    def hook_sim_end(self):
        self.process(sim.stats.get('performance_model', 0, 'elapsed_time'))
        bullet_stop()

    def process(self, time):
        time = coarse(time)
        sim.stats.write(str(time))
        if self.t_last: self.compute_power(self.t_last, time)
        self.t_last = time

    def compute_power(self, t0, t1):
        filebase = os.path.join(output, 'power-%s-%s-%s' % (t0, t1, t1 - t0))
        bullet_send(filebase, t0, t1)

def coarse(time):
    return long(long(time) / sim.util.Time.NS)

def bullet_send(filebase, t0, t1):
    prepare = "%s -o %s -d %s --partial=%s:%s" % (mcpat_bin, filebase, output, t0, t1)
    enqueue = "(%s RPUSH %s %s > /dev/null)" % (redis_bin, queue, filebase + '.xml')
    run('unset PYTHONHOME && %s && %s &' % (prepare, enqueue))

def bullet_start():
    run('%s -s %s -d %s -c &' % (bullet_bin, server, database))

def bullet_stop():
    run('%s RPUSH %s bullet:halt > /dev/null' % (redis_bin, queue))

def die(message):
    print('Error: %s.' % message)
    sys.exit(1)

def report(message):
    print('-------> %s' % message)

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

sim.util.register(Bullet())
