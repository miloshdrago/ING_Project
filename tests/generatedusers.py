#!/usr/bin/env python3

# dependencies
import simpy
import simpy.rt
import random
from functools import partial, wraps
import matplotlib.pyplot as plt

# configuration vars
RANDOM_SEED = 64
N_USERS = 200
N_INTERVAL = 1

# monitored server data
monitored = []

# set the random seed
random.seed(RANDOM_SEED)

def server_monitor(resource, pre=None, post=None):
    """
    Function to patch a server resource to monitor a server.
    """
    def get_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # call the handler before the resource operation
            if pre:
                pre(resource)

            # get the resource operation value
            ret = func(*args, **kwargs)

            # call the handler after the resource operation
            if post:
                post(resource)
            
            # expose the operation return value
            return ret
        # expose the wrapper
        return wrapper

    # wrap the request operations
    if hasattr(resource, 'request'):
        setattr(resource, 'request', get_wrapper(getattr(resource, 'request')))

def monitor(data, resource):
    """Function to monitor a server."""
    data.append((
        resource._env.now,
        resource.count
    ))

def request(env, server, user, transaction):
    """Function as process of a request of a transaction."""        
    print("requesting a transaction for user {} at {}".format(user, env.now))

    # we need to ask the server to process our request
    with server.request() as req:

        # tell others we made a request
        yield req

        # tell others about the process of the request
        yield process(env, user, transaction)
        print("processed transaction for user {} at {}".format(user, env.now))

def process(env, user, transaction):
    """Function as process of processing a request of a transaction.""" 
    print("processing a transaction for user {} at {}".format(user, env.now))

    # larger transactions take more time to process
    if transaction > 100:
        return env.timeout(3)

    # regular transactions take little time to process
    else:
        return env.timeout(1)

def source(env, server, users, interval):
    """Function as process of generating new transaction requests from users."""

    # add a number of users
    for n in range(users):

        # process a new request
        env.process(request(env, server, n, random.randint(50, 150)))

        # we need to wait for the next users to request transactions
        yield env.timeout(random.expovariate(1.0 / interval))


# we need a new environment
env = simpy.RealtimeEnvironment(factor=60, strict=True)

# we need a new server
server = simpy.Resource(env, capacity=10)

# bind the monitored data to the monitor
monitor = partial(monitor, monitored)

# install a server monitor
server_monitor(server, pre=monitor)

# start generating users
env.process(source(env, server, N_USERS, N_INTERVAL))

# run the simulation
env.run()

# output monitored server data
x = [t for (t, n) in monitored]
y = [n for (t, n) in monitored]
plt.plot(x, y)
plt.xlabel('simulation time passed')
plt.ylabel('active transaction requests')
plt.show()