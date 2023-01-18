import simpy # SimPy useful video - https://youtu.be/G2WftFiBRFg?list=PLkilSo1vpRstA9ptjga71zdoUNUsm43ba
import numpy as np

# note: times are expressed in hours

# --- Global variables
man_hours_worked = 0 # total number of man hours worked
hour_passed = 0      # total number of hours passed
# ---

#
# Class for a single worker
class Worker:
  def __init__(self, id, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time) -> None:
    self.id = id
    self.avg_session_time = avg_session_time
    self.max_working_sessions = max_working_sessions
    self.long_resting_time = long_resting_time
    self.avg_short_resting_time = avg_short_resting_time
    self.hours_worked = 0      # total number of hours worked
    self.working_sessions = 0  # number of sessions of work
  
  #
  # Return the number of hours worked in a single session
  def work(self):
    hour = abs(np.random.normal(self.avg_session_time, 0.1))
    self.hours_worked = self.hours_worked + hour
    self.working_sessions = self.working_sessions + 1
    return hour
  
  #
  # Does the worker need a long rest?
  def need_long_rest(self):
    return self.working_sessions >= self.max_working_sessions
  
  #
  # The worker perform a long rest (after a number of working sessions)
  def long_rest(self):
    self.hours_worked = 0
    return self.long_resting_time
    
  #
  # The worker perform a short rest after a working session
  def short_rest(self):
    rest_time = abs(np.random.normal(self.avg_short_resting_time, 0.1))
    return rest_time

#
# Class for all tunner workers
class TunnelWorkers:
  def __init__(self, env, num_workers, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time) -> None:
    self.env = env
    self.staff = simpy.Store(env)
    for i in range(num_workers):
      self.staff.put(Worker(i, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time))
    self.at_work = 0
  
  #
  # Handle both short and long resting of a worker
  def handle_resting(self, request, worker):
    if worker.need_long_rest():
      yield self.env.timeout(worker.long_rest())
    else:
      yield self.env.timeout(worker.short_rest())
    
    # the worker becomes available again
    self.staff.put(request)

  #
  # Handle a working slot
  def handle_working_slot(self, slot):
    global man_hours_worked
    global hour_passed
    
    while True:
      # wait for the first available worker
      request = self.staff.get()
      yield request

      # --- unclear why I need to do this
      worker = request.value
      while not isinstance(worker, Worker):
        worker = worker.value
      # ---

      self.at_work = self.at_work + 1
      print(f"{self.env.now:.2f}: {self.at_work} workers at slot {slot} for {man_hours_worked:.2f}")

      work_time = worker.work()
      yield self.env.timeout(work_time)
      man_hours_worked = man_hours_worked + work_time
      
      self.at_work = self.at_work - 1
      print(f"{self.env.now:.2f}: {self.at_work} workers at slot {slot} for {man_hours_worked:.2f}")
      
      self.env.process(self.handle_resting(request, worker))

#
# SimPy process setup
def setup(env,  max_working_slots, num_workers, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time):
  global hour_passed
  tunnelWs = TunnelWorkers(env, num_workers, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time)
  for slot in range(max_working_slots):
    env.process(tunnelWs.handle_working_slot(slot + 1))
  
  while True:
    hour_passed = hour_passed + 1
    yield env.timeout(1)

#
# SimPy simulation
def simpy_simulation(simulation_time, max_working_slots, num_workers, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time):
  global man_hours_worked, hour_passed
  man_hours_worked = 0
  hour_passed = 0

  print("====== Starting simulation ======")
  env = simpy.Environment()
  env.process(setup(env, max_working_slots, num_workers, avg_session_time, max_working_sessions, long_resting_time, avg_short_resting_time))
  env.run(until=simulation_time)
  print("=================================")

  print(f"Man-hours worked: {man_hours_worked:.2f}")
  print(f"Hour passed: {hour_passed}")
  return man_hours_worked

#
# Main
#

if __name__ == "__main__":
  NUM_WORKERS = 15 # number of workers
  MAX_WORKING_SLOTS = 7 # number of workers that can work simultaneously
  AVG_SESSION_TIME = 1 # average working time for a session
  AVG_SHORT_RESTING_TIME = 0.25 # average resting time after a working session
  MAX_WORKING_SESSIONS = 7 # maximum number of working sessions
  LONG_RESTING_TIME = 14 # "long" resting time after the maximum number of working sessions
  SIMULATION_TIME = 24 * 10 # 10 days of simulation time 

  simpy_simulation(SIMULATION_TIME, MAX_WORKING_SLOTS, NUM_WORKERS, AVG_SESSION_TIME, MAX_WORKING_SESSIONS, LONG_RESTING_TIME, AVG_SHORT_RESTING_TIME)