"""
Class for acting as a server inside of a simpy simulation. This server is nothing
more than a resource with some additional patches.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   lib/Server.py
"""

# dependencies
from simpy import PreemptiveResource
from numpy.random import exponential

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
        """
        # call the parent constructor
        super().__init__(*args)

        # reference to the environment and capacity
        self._env = args[0]
        self._capacity = args[1]

        # setup the initial state of this server
        self._state = {
            'name':  "%s#%s" % (kwargs['kind'], kwargs['uuid']),
            'kind':  kwargs['kind'],
            'time':  round(self._env.now, 4),
            'queue': len(self.queue),
            'users': self.count,
            'cpu': 0,
            'memory': 0,
            'latency': 0
        }

    @property
    def environment(self):
        """
        Getter to expose the environment.
        
        Returns
        -------
        Environment
        """
        return self._env

    @property
    def capacity(self):
        """
        Getter to expose the server capacity.

        Returns
        -------
        int
        """
        return self._capacity

    def request(self, *args, **kwargs):
        """
        Method override to request a context in which this resource can be accessed.
        @see https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html#simpy.resources.resource.Request

        Keyworded parameters
        ----------
        process_id: int
            ID of the current processes requesting this server.
        requested_by: string
            Name of the entity that requested this process (e.g. client or another
            server).
        message: string
            Description of the request.
        priority: int
            See simpy.PreemptiveResource.request.
        """
        # update the state of the server
        self._state.update(
            time=round(self._env.now, 4),
            queue=len(self.queue),
            users=self.count,
            cpu=self.cpu(),
            memory=self.memory(),
            latency=self.latency()
        )

        # we need to update the state with the current process id, so we can
        # track this process later on
        state = self._state.copy()
        state.update({
            "id": kwargs['process_id'] if 'process_id' in kwargs else None,
            "requested_by": kwargs['requested_by'] if 'requested_by' in kwargs else None,
        })

        # the message that describes this request
        message = kwargs['message'] if 'message' in kwargs else "Requesting"

        # we need to construct a logmessage, which we can log on this server
        # and push onto the environment
        msg = f"{state['time']};{state['requested_by']};INFO;{state['cpu']};{state['memory']};{state['latency']};{state['id']};{state['name']};{message}"

        # push the log to the environment
        self._env.log(msg)

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
        return self._state

    def latency(self):
        """
        Method to expose the server latency.

        Returns
        -------
        float
        """
        # expose a random value based on an exponential distribution, scaled
        # with the cpu time
        return exponential(self.cpu())

    def memory(self):
        """
        Method to expose the server's memory usage.

        Returns
        -------
        float
        """
        # get the current state
        state = self.state()

        # expose the calculated memory usage based on the queue, users, and
        # scaled capacity
        return (state['users'] + state['queue']) / (self.capacity * 10)

    def cpu(self):
        """
        Method to expose the server's cpu usage.

        Returns
        -------
        float
        """
        # get the current state
        state = self.state()

        # expose the cpu load
        return state['users'] / self.capacity
