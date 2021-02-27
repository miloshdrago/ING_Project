"""
Class for setting up a pool of servers. This can be used to pool
a given number of servers and get access to an available one.

@file   lib/Servers.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from lib.Server import Server
from uuid import uuid4
from numpy.random import randint, shuffle


class Servers(object):

    def __init__(self, env, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        env: Environment
            The environment this pool is using.

        Keyworded parameters
        --------------------
        size: integer
            Size of the pool, i.e. the number of servers.
            Default: 10.
        capacity: integer
            Capacity of each server.
            Default: 10.
        kind: string
            Kind of servers in this pool.
            Default: 'regular'.
        """
        # set the default arguments
        size = kwargs['size'] if 'size' in kwargs else 10
        capacity = kwargs['capacity'] if 'capacity' in kwargs else 10
        kind = kwargs['kind'] if 'kind' in kwargs else 'regular'

        # construct a new pool
        self._pool = [Server(env, capacity, uuid=uuid4(), kind=kind) for _ in range(size)]

        # assign some parameters as properties
        self._kind = kind

        # disabled state of this pool
        self._disabled = False

        # random state of this pool
        self._random = False

        # stuck loadbalancing state of this pool
        self._stuck = False
        self.stuckserver = None

    def kind(self):
        """
        Getter to expose the kind of this server pool.

        Returns
        -------
        string
        """
        return self._kind

    def disabled(self, state):
        """
        Method to disable this pool of servers. This will make sure that no
        server is available anymore.

        Parameters
        ----------
        state: bool
            Disabled or not.

        Returns
        -------
        self
        """

        # change the disabled state
        self._disabled = bool(state)

        # allow chaining
        return self

    def random(self, state):
        """
        Method to change the allocation to a random server instead on the
        server with the lowest number of users in queue

        Parameters
        ----------
        state: bool
            Random or not.

        Returns
        -------
        self
        """

        # change the random state
        self._random = bool(state)

        # allow chaining
        return self

    def stuck(self, state):
        """
        Method to set the allocation stuck on one server instead of spreading
        over te entire pool.

        Parameters
        ----------
        state: bool
            Stuck or not.

        Returns
        -------
        self
        """

        # change the random state
        self._stuck = bool(state)

        # If set to stuck, pick random server in pool to keep sending messages to
        self.stuckserver = self._pool[randint(0, len(self._pool))]

        # allow chaining
        return self

    def server(self, **kwargs):
        """
        Method to get access to an available server from the pool.

        Keyworded parameters
        --------------------
        exclude: list
            Collection of servers to exclude from the pool when looking for
            a new server.

        Returns
        -------
        Server|None
        """
        # check if we are disabled
        if self._disabled:
            return None

        # we need a reference to the pool of servers
        pool = self._pool

        # we need to check if we need to pick a server randomly, or by lowest
        if self._random:

            # pick a random server
            return pool[randint(0, len(pool))]

        # we need to check if the loadbalancing is stuck on one server
        if self._stuck:

            # pick a random server
            return self.stuckserver

        # we need a reference to the server with the lowest number of
        # processes in queue, which is the server that is going to
        # be targeted
        lowest = None

        # we need to check if we have a list of servers that we need to exclude
        # from the pool of servers
        exclude = kwargs['exclude'] if 'exclude' in kwargs else []

        # we need to iterate over the pool of servers, so we can check
        # the state of each server and find the one with the least
        # amount of traffic
        # Shuffle to get spread in a low volume system
        shuffle(pool)
        for server in pool:

            # state of the current server
            current = server.state()

            # pass servers that we need to exclude
            if server in exclude:
                continue

            # assign a new server as the lowest
            if lowest is None:
                lowest = server

            # assign a new server if has a lower number of processes
            # in the queue
            elif current['queue'] < lowest.state()['queue']:
                lowest = server

        # expose the server with the lowest number of processes in the queue
        return lowest

    def get_random(self, **kwargs):
        """
        Method to get access to an random server from the pool for use in error generation

        Returns
        -------
        Server
        """
        # we need a reference to the pool of servers
        pool = self._pool

        # pick a random server
        return pool[randint(0, len(pool))]
