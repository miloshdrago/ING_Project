#!/usr/bin/env python3

# dependencies
import unittest
import simpy
import simpy.rt
import random
import time
import datetime

# set random seed to keep consistency
random.seed(64)

class SimpleTransaction(object):
    """
    Class to represent a simple transaction in a network system.
    """

    def __init__(self, env, servers, n):
        """
        Constructor.

        Parameters
        ----------
        env: simpy.Environment
            Simulated environment to run the transaction in.
        servers: simpy.Resource
            Shared resource to send transactional requests to.
        n: int
            Identifier for a transaction.
        """
        self.env = env
        self.process = self.env.process(self.request())
        self._servers = servers
        self._id = n

    def log(self, msg):
        """
        Method to log out a process.

        Parameters
        ----------
        msg: string
            Description of the process to log.
        """
        print(msg, self._id, datetime.datetime.fromtimestamp(time.time()), sep=",")

    def request(self):
        """
        Generator method to process a transaction.
        """
        self.log("requesting a transaction")

        # we need a random transaction time
        transaction_time = random.randint(0, 5)

        # we need to request access to a server
        with self._servers.request() as req:

            # expose the request to tell others a transaction is active
            yield req

            # process the transaction for five seconds
            self.log("processing a transaction")
            yield self.env.timeout(transaction_time)
            self.log("processed a transaction")

class SimpleTransactionTestCase(unittest.TestCase):
    """
    Test case for the simulation of a simple financial transaction. This transaction
    encompasses the following steps:

        1. request transaction
            value = x

        2. request is sent to a server
            servers_available = y

        3. server processes transaction
            processing_time = z

        4. server responds with a success
            respond_time = q

        5. end transaction
    
    Time in the simulation can be interpreted as seconds.
    """

    def test_transaction(self):
        
        # we need a new environment
        env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=True)

        # we need servers to process the transaction
        servers = simpy.Resource(env, capacity=3)

        # start a number of transactions
        for n in range(20):

            # request a new transaction
            transaction = SimpleTransaction(env, servers, n)

        # run the simulation
        env.run(until=10)

# run test as main
if __name__ == "__main__":
    unittest.main()