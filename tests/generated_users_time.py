#!/usr/bin/env python3

# dependencies
import simpy
import simpy.rt
import random
from functools import partial, wraps
import matplotlib.pyplot as plt
import scipy.stats as stats
from collections import deque
import logging
logging.basicConfig(filename="example.log", level=logging.DEBUG)

# configuration vars
RANDOM_SEED = 42
S_SERVER = 100
N_FRACTION = 60 # seconds
N_SIMULATION = 60 * 60 # seconds
T_SIMULATION = N_SIMULATION / N_FRACTION

t = 60 # minutes
rate = 1000 * t # 1000 per minute

# set the random seed
random.seed(RANDOM_SEED)

# monitored server data
monitored = []

# distribution of user transactions
dist = stats.poisson.rvs(mu=rate, size=t, random_state=RANDOM_SEED)

dist = stats.poisson.rvs(mu=rate*24, size=24, random_state=RANDOM_SEED)

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
    logging.info("requesting a transaction for user {} at {}".format(user, env.now))

    # we need to ask the server to process our request
    with server.request() as req:

        # tell others we made a request
        yield req

        # tell others about the process of the request
        yield process(env, user, transaction)
        logging.info("processed transaction for user {} at {}".format(user, env.now))

def process(env, user, transaction):
    """Function as process of processing a request of a transaction.""" 
    logging.info("processing a transaction for user {} at {}".format(user, env.now))

    # larger transactions take more time to process
    if transaction > 100:
        logging.warning('large transaction')
        return env.timeout(3)

    # regular transactions take little time to process
    else:
        return env.timeout(1)

def source(env, server):
    """Function as process of generating new transaction requests from users."""

    # add a number of users
    for t in dist:

        # process a new request for each user
        for n in range(t):
            env.process(request(env, server, n, random.randint(50, 150)))

        # we need to wait for the next users to request transactions
        yield env.timeout(N_FRACTION)

# we need a new environment
env = simpy.Environment()

# we need a new server
server = simpy.Resource(env, capacity=S_SERVER)

# bind the monitored data to the monitor
monitor = partial(monitor, monitored)

# install a server monitor
server_monitor(server, pre=monitor)

# start generating users
env.process(source(env, server))

# run the simulation
env.run(until=N_SIMULATION)
