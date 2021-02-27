"""
Class for setting up a pool of multiple pools of servers. Each pool could contain
a different type of server. For example, having a multiserver system of pools
containing: regular servers, balance servers, web servers, etc. Each of these
should process different actions (conceptually).

@file   lib/MultiServers.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

from random import choice


class MultiServers(object):

    def __init__(self):
        """
        Constructor.
        """
        # we need an empty collection to hold all pools
        self._pools = {}

    def append(self, pool):
        """
        Method to append a new pool to the pools.

        Parameters
        ----------
        pool: Servers
            Pool to add to the collection.

        Returns
        -------
        self
        """
        # called as setter
        self._pools[pool.kind()] = pool

        # allow chaining
        return self

    def get(self, kind):
        """
        Method to get to find the server pool of the given kind.

        Parameters
        ----------
        kind: string
            Kind of servers for that pool (e.g. regular).

        Returns
        -------
        Servers|None
        """
        # expose the pool if it exists
        if kind not in self._pools:
            # Remove for final version
            print(f"Kind: {kind} not found in pools {self._pools}")
        return self._pools[kind] if kind in self._pools else None

    def random_pool(self):
        """
        Method to get random server pool to break a server.

        Returns
        -------
        Server pool
        """
        return choice(list(self._pools.values()))
