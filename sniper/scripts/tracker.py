import os, sim

mcpat = os.path.join(os.getenv('SNIPER_ROOT'), 'tools/mcpat.py')
output = sim.config.output_dir
period = 1e6 * sim.util.Time.NS

def coarse(time):
  return long(long(time) / sim.util.Time.NS)

def report(message):
  print("-------> %s" % message)

class Tracker:
  def setup(self, args):
    sim.util.Every(period, self.periodic, roi_only = True)
    self.t_last = 0

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
    command = 'unset PYTHONHOME; %s -d %s -o %s --partial=%s:%s --no-graph --no-text' % (
      mcpat, output, filename, t0, t1
    )
    os.system(command)

sim.util.register(Tracker())
