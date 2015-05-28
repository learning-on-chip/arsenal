import os, sim

period = 1e6 * sim.util.Time.NS

def coarse(time):
  return long(long(time) / sim.util.Time.NS)

def report(message):
  print("[TRACKER] %s" % message)

class Tracker:
  def setup(self, args):
    sim.util.Every(period, self.periodic, roi_only = True)
    self.t_last = 0

  def periodic(self, time, delta):
    report("Time %.2f ms, delta %.2f ms" % (
      time / sim.util.Time.MS, delta / sim.util.Time.MS
    ))
    time = coarse(time)
    sim.stats.write(str(time))
    self.compute_power(self.t_last, time)
    self.t_last = time

  def hook_sim_end(self):
    time = coarse(sim.stats.get('performance_model', 0, 'elapsed_time'))
    self.compute_power(self.t_last, time)
    self.t_last = time

  def compute_power(self, t0, t1):
    _t0 = t0 or 'roi-begin'
    _t1 = t1 or 'roi-end'
    command = 'unset PYTHONHOME; %s -d %s -o %s --partial=%s:%s --no-graph --no-text' % (
      os.path.join(os.getenv('SNIPER_ROOT'), 'tools/mcpat.py'), sim.config.output_dir,
      os.path.join(sim.config.output_dir, 'power-%s-%s-%s' % (t0, t1, t1 - t0)), _t0, _t1
    )
    os.system(command)

sim.util.register(Tracker())
