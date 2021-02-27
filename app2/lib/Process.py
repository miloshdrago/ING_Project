"""
Class to act as base class for all processes within a simulation. This
class should not be instantiated directly, but inherited from if you
want to specify your own process.

@file   lib/Process.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from abc import ABCMeta, abstractmethod

class Process(metaclass=ABCMeta):

    def __init__(self, environment, servers):
        """
        Constructor.

        Parameters
        ----------
        environment: simpy.Environment
            The environment the process is running in.
        servers: MultiServers
            The pool of pools of servers from which you can access them.
        """
        self._env = environment
        self._servers = servers

        # we need to run this process immediately and expose the process as
        # public which allows others to interfere with it, which is allowed.
        # this could be useful for, for example, introducing errors.
        self.process = self._env.process(self.run())

    @property
    def environment(self):
        """
        Getter for exposing the environment.

        Returns
        -------
        Environment
        """
        return self._env

    def servers(self, kind):
        """
        Method to get access to a pool of servers given
        to this process.

        Parameters
        ----------
        kind: string
            Kind of server pool to get access to.

        Returns
        -------
        Servers
        """
        return self._servers.get(kind)

    @abstractmethod
    def run(self):
        """
        Generator method to run as simpy process.
        This needs to be implemented by child classes.

        Yields
        ------
        simpy.Timeout or simpy.Process
        """
        pass
