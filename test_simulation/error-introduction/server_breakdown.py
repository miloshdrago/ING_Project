"""
Server Breakdown DES Simulation

Covers:

- Interrupts
- Resources: PreemptiveResource

Scenario:
  A system has *n* identical servers. A stream of jobs (enough to
  keep the servers busy) arrives. Each server breaks down
  periodically. Repairs are carried out by one repairman/engineer. The repairman
  has other, less important tasks to perform, too. Broken servers
  preempt theses tasks. The repairman continues them when he is done
  with the server repair. The system works continuously.

To run:
  python server_breakdown.py

"""
import random
import simpy


RANDOM_SEED = 42
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 300.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME = 30.0     # Time it takes to repair a server in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_SERVERS = 10      # Number of servers in the system
WEEKS = 4            # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes


def time_per_transaction():
    """Return actual processing time for a transaction (or any other server job)."""
    return random.normalvariate(PT_MEAN, PT_SIGMA)


def time_to_failure():
    """Return time until next failure for a server."""
    return random.expovariate(BREAK_MEAN)


class Server(object):
    """A server produces jobs and my get broken every now and then.

    If it breaks, it requests a *repairman* and continues the production
    after the it is repaired.

    A server has a *name* and a numberof *jobs_made* thus far.

    """
    def __init__(self, env, name, repairman):
        self.env = env
        self.name = name
        self.jobs_made = 0
        self.broken = False

        # Start "working" and "break_server" processes for this server.
        self.process = env.process(self.working(repairman))
        env.process(self.break_server())

    def working(self, repairman):
        """Processes transactions/jobs as long as the simulation runs.

        While processing, the server may break multiple times.
        Requests a repairman when this happens.

        """
        while True:
            # Start making a new job
            done_in = time_per_transaction()
            while done_in:
                try:
                    # Working on the job
                    start = self.env.now
                    yield self.env.timeout(done_in)
                    done_in = 0  # Set to 0 to exit while loop.

                except simpy.Interrupt:
                    self.broken = True
                    done_in -= self.env.now - start  # How much time left?

                    # Request a repairman. This will preempt its "other_job".
                    with repairman.request(priority=1) as req:
                        yield req
                        yield self.env.timeout(REPAIR_TIME)

                    self.broken = False

            # Job is done.
            self.jobs_made += 1

    def break_server(self):
        """Break the server every now and then."""
        while True:
            yield self.env.timeout(time_to_failure())
            if not self.broken:
                # Only break the server if it is currently working.
                self.process.interrupt()


def other_jobs(env, repairman):
    """The repairman's other (unimportant) job."""
    while True:
        # Start a new job
        done_in = JOB_DURATION
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of server repairs.
            with repairman.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    done_in -= env.now - start


# Setup and start the simulation
print('Server network system')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
repairman = simpy.PreemptiveResource(env, capacity=1)
servers = [Server(env, 'server %d' % i, repairman)
            for i in range(NUM_SERVERS)]
env.process(other_jobs(env, repairman))

# Execute!
env.run(until=SIM_TIME)

# Analyis/results
print('Server network system results after %s weeks' % WEEKS)
for server in servers:
    print('%s processed %d jobs.' % (server.name, server.jobs_made))


