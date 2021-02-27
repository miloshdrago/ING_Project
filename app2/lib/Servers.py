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
from numpy.random import randint

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
        size     = kwargs['size'] if 'size' in kwargs else 10
        capacity = kwargs['capacity'] if 'capacity' in kwargs else 10
        kind     = kwargs['kind'] if 'kind' in kwargs else 'regular'

        # construct a new pool
        self._pool = [Server(env, capacity, uuid=uuid4(), kind=kind) for _ in range(size)]

        # assign some parameters as properties
        self._kind = kind

        # disabled state of this pool
        self._disabled = False

    @property
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

    def server(self, **kwargs):
        """
        Method to get access to an available server from the pool.

        Keyworded parameters
        --------------------
        exclude: list
            Collection of servers to exclude from the pool when looking for
            a new server.
        random: bool
            Get access to a randomly picked server, and not the one with the
            lowest number of users in queue.

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
        random = kwargs['random'] if 'random' in kwargs else False

        # check if we need to find a random one
        if random:

            # pick a random server
            return pool[randint(0, len(pool))]

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

