from numpy.random import uniform


class ErrorGenerator(object):

    def __init__(self, envoirment, servers, errorwait, error_duration, *args, **kwargs):
        """

        Parameters
        ----------
        envoirment: instance of Envoirment class
        servers: instance of MultiServers pool
        """

        # Set serverpools
        self._pools = servers

        # Set simpy Envoirment
        self._env = envoirment

        self.errorwait = errorwait
        self.error_duration = error_duration

        # Initialize error generator
        self.error_generator = envoirment.process(self.error_generator())

    def error_generator(self):
        while True:
            # Wait a random amount of time to introduce the error
            yield self._env.timeout(uniform(*self.errorwait))

            # Get random server
            server = self._pools.random_pool().get_random()
            # Write to error log
            self._env.log(
                message=f'{self._env.now};{server.state()["name"]};Block;Start', type="error")
            # Make an equal amount of requests to the capacity of the server
            # Make a list of requests
            request_list = [server.request(priority=0) for i in range(server.capacity)]
            for request in request_list:
                yield request  # Send priority request to PreemptiveResource
            # Wait for the error to be resolved
            yield self._env.timeout(uniform(*self.error_duration))
            # Release spots in server when the error is resolved
            for request in request_list:
                yield server.release(request)
            # Write to error log
            self._env.log(
                message=f'{self._env.now};{server.state()["name"]};Block;Stop', type="error")
