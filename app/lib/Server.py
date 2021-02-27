"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Server.py
"""

# dependencies
from simpy import PreemptiveResource
from numpy.random import exponential, uniform


class Server(PreemptiveResource):

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        @see simpy.Resource

        Keyworded arguments
        -------------------
        uuid: string
            UUID as identifier for this server.
        kind: string
            Kind of the server (e.g. balance, regular, database).

        Optiomal Keyworded arguments
        memmax: integer:
            Set scalar how many times the max capacity fits in memory
            Default = 10
        """
        # call the parent constructor
        super().__init__(*args)

        # reference to the environment and capacity
        self._env = args[0]

        # Set memory max capacity
        if 'memmax' in kwargs:
            self.memmax = kwargs['memmax']
        else:
            # Default is 10 times the capacity
            self.memmax = 10

        # Set latencyscaler capacity
        if 'latencyscaler' in kwargs:
            self.latencyscaler = kwargs['latencyscaler']
        else:
            # Default is 1 times the capacity
            self.latencyscaler = 1

        # setup the initial state of this server
        self._state = {
            'name':  "%s#%s" % (kwargs['kind'], kwargs['uuid']),
            'kind':  kwargs['kind'],
            'queue': len(self.queue),
            'users': self.count,
            'cpu': 0,
            'memory': 0,
            'latency': 0,
        }

    def environment(self):
        """
        Getter to expose the environment.

        Returns
        -------
        Environment
        """
        return self._env

    def get_capacity(self):
        """
        Getter to expose the server capacity.

        Returns
        -------
        int
        """
        return self.capacity

    def request(self, *args, **kwargs):
        """
        Method override to request a context in which this resource can be accessed.
        @see https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#simpy.resources.resource.Request

        Keyworded parameters
        ----------
        priority: int
            See simpy.PreemptiveResource.request.
        """

        # parse parameters for the super class method
        priority = kwargs['priority'] if 'priority' in kwargs else 1

        # call the parent class for the original method
        return super().request(priority=priority)

    def state(self):
        """
        Method to expose the current state of a server.

        Returns
        -------
        dict
        """

        self._state.update(queue=len(self.queue),
                           users=self.count,
                           cpu=self.cpu(),
                           memory=self.memory(),
                           latency=self.latency()
                           )

        return self._state

    def latency(self):
        """
        Method to expose the server latency.

        Returns
        -------
        float
        """
        # state = self.state()

        # Temporalily update the amount of users by adding one to reflect the
        # incoming transaction

        # expose a random value based on an exponential distribution, scaled
        # with the cpu usage
        # return exponential(self.cpu())

        latency = exponential(self.cpu()) * self.latencyscaler

        return latency

    def memory(self):
        """
        Method to expose the server's memory usage.

        Returns
        -------
        float
        """
        # # get the current state
        # state = self.state()

        # expose the calculated memory usage based on the queue, users, and
        # scaled capacity
        return (self.count + len(self.queue)) / (self.capacity * self.memmax)

    def cpu(self):
        """
        Method to expose the server's cpu usage.

        Optional parameters:
        addition (defaul = 0), possibility to add user to keep values non-zero

        Returns
        -------
        float
        """
        # # get the current state
        # state = self.state()

        # expose the cpu load
        return self.count / self.capacity

    def faulty_patch(self, state):
        # error function to increase the latency scaler tenfold when true
        if state:
            self.latencyscaler = 10
        if not state:
            self.latencyscaler = 1
