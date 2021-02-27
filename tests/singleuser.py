#!/usr/bin/env python3

# dependencies
import simpy

def request(env, server, transaction):
    """Function as process of a request of a transaction."""
    while True:
        
        print("requesting a transaction at {}".format(env.now))

        # we need to ask the server to process our request
        with server.request() as req:

            # tell others we made a request
            yield req

            # tell others about the process of the request
            yield process(env, transaction)
            print("processed transaction at {}".format(env.now))

def process(env, transaction):
    """Function as process of processing a request of a transaction.""" 
    print("processing a transaction at {}".format(env.now))

    # larger transactions take more time to process
    if transaction > 100:
        return env.timeout(3)

    # regular transactions take little time to process
    else:
        return env.timeout(1)

# we need a new environment
env = simpy.Environment()

# we need a new server
server = simpy.Resource(env, capacity=1)

# process a new request
env.process(request(env, server, 50))

# run the simulation
env.run(until=10)