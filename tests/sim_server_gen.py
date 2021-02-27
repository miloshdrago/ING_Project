#!/usr/bin/env python3

# dependencies
import simpy
from src.TransactionGenerator import TransactionGenerator
from src.Server import Server
from uuid import uuid4
import logging

# we need a new generator
gen = TransactionGenerator()

# we need a sample datasets
data = gen.hourly()

def request(env, server, user):
    """Function as process of a request of a transaction."""        
    #print("requesting transaction - {} - {}".format(user, env.now))

    # we need to ask the server to process our request
    with server.request() as req:

        # tell others we made a request
        yield req

        # it takes time to process
        yield env.timeout(server.latency())

def source(env, server):
    """Function as process of generating new transaction requests from users."""

    # we need to iterate over all transaction timestamps
    for t in data:

        # we need to iterate over the number of transactions for a timestamp
        for k in range(t):
            env.process(request(env, server, k))

        # we need to prepare a timeout, which will indicate when the next
        # batch of transactions are coming in
        timeout = 1 / gen.MINUTE

        # log the current state of the server to the server log
        server_state = server.state()
        server_state['upcoming'] = env.now 
        server.log(server_state)

        # we need to wait for the next users to request transactions
        yield env.timeout(timeout)

# set the logging environment
logging.basicConfig(level=logging.DEBUG)

# we need a new environment
env = simpy.Environment()

# we need a new server
server = Server(uuid4(), env, capacity=50000)

# start generating users
env.process(source(env, server))

# run the simulation
env.run(until=gen.MINUTE)
