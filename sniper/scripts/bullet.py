import os, sim, sys

output = sim.config.output_dir
period = 1e6 * sim.util.Time.NS

mcpat = os.path.join(os.getenv('TOOLS_ROOT'), 'mcpat.py')
if not os.path.exists(mcpat): die('cannot find mcpat.py')

bullet = os.path.join(os.getenv('BULLET_ROOT'), 'bin', 'bullet')
if not os.path.exists(bullet): die('cannot find bullet')

database = os.path.join(output, 'database.sqlite3')

class Bullet:
    def setup(self, args):
        self.first = True
        self.t_last = 0
        sim.util.Every(period, self.periodic, roi_only = True)

    def periodic(self, time, elapsed):
        report("Time %.2f ms, elapsed %.2f ms" % (
            time / sim.util.Time.MS, elapsed / sim.util.Time.MS
        ))
        self.process(time)

    def hook_sim_end(self):
        self.process(sim.stats.get('performance_model', 0, 'elapsed_time'))

    def process(self, time):
        time = coarse(time)
        sim.stats.write(str(time))
        if self.t_last: self.compute_power(self.t_last, time)
        self.t_last = time

    def compute_power(self, t0, t1):
        filename = os.path.join(output, 'power-%s-%s-%s' % (t0, t1, t1 - t0))
        mcpat_run(filename, t0, t1)
        filename = filename + '.xml'
        if self.first:
            bullet_prepare(filename)
            self.first = False
        bullet_run(filename, t0, t1)

def coarse(time):
    return long(long(time) / sim.util.Time.NS)

def bullet_run(filename, t0, t1):
    run('%s -c %s -d %s' % (bullet, filename, database))

def bullet_prepare(filename):
    run('%s -c %s -d %s -p' % (bullet, filename, database))

def die(message):
    print("Error: %s." % message)
    sys.exit(1)

def mcpat_run(filename, t0, t1):
    run('unset PYTHONHOME; %s -o %s -d %s --partial=%s:%s' % (
        mcpat, filename, output, t0, t1
    ))

def report(message):
    print("-------> %s" % message)

def run(command):
    if os.system(command) != 0: die('failed to run `%s`' % command)

sim.util.register(Bullet())
