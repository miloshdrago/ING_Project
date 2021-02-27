"""
Class for

@author Tycho Atsma <tycho.atsma@gmail.com>
        Joris van der Vorst <joris@jvandervorst.nl>
@file   lib/Processor.py
@scope  private
"""

# 3rd party dependencies
from uuid import uuid4
from simpy import Interrupt
from simpy.resources.resource import Preempted
import pandas as pd
from numpy.random import randint


class MessageGenerator(object):

    def __init__(self, envoirment, servers, seasonality, *args, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        envoirment: instance of Envoirment class
        servers: instance of MultiServers pool
        seasonality: Seasonality
            Source of incoming messages.
            [required]

        Keyworded parameters
        --------------------
        kinds: list
            List of server kinds as sequence.
            [optional]
        """

        # required seasonality
        self._seasonality = seasonality

        # Set serverpools
        self._pools = servers

        # Set simpy Envoirment
        self._env = envoirment

        # optional sequence of kinds
        self._kinds = kwargs['kinds'] if 'kinds' in kwargs else ['regular']

        # optional timeout duration
        self._timeout = kwargs['timeout'] if 'timeout' in kwargs else 1

        self.excludeservers = []

        # Initialize message generator
        self.messages_process = envoirment.process(self.generate())

    def generate(self):
        """
        Generator method to create requests.

        Yields
        ------
        simpy.Process
        """
        # run indefinitely
        while True:

            # timeout before proceeding to the next transaction
            yield self._env.timeout(self._seasonality.interval())

            # id of the current request
            process_id = uuid4()

            # init a new request
            clientrequest = self._env.process(self.client_request(process_id))
            # process = Subprocess(self.environment, self._servers, kinds=self._kinds).process

            # yield clientrequest

    def client_request(self, process_id):
        """
        Client request consisting of messages to a sequence of servers.

        Parameters
        ----------
        process_id: uuid4 of request
        """

        # Set sequence of Servers
        kinds = self._kinds

        # collection of servers processing a request
        request_df = pd.DataFrame(
            columns=["kind", "open_servers", "open_requests"])

        route = []
        # get the client who requested this process
        route.append({"name": 'client', "kind": "client"})

        # we need to iterate over all kinds
        for (idx, kind) in enumerate(kinds):

            current_message = []

            # Get server that requests the message
            requested_by = route[idx]

            # reference to a return loop
            return_loop = None

            # Test if request is back at a previously accessed server
            if kind in request_df["kind"].values:

                # Remember first location of server
                return_loop = request_df.index[request_df['kind'] == kind].tolist()

                # Get same server as before:
                server = request_df.loc[return_loop[0], "open_servers"]

            else:
                # we need to get access to a server pool
                pool = self._pools.get(kind)
                server = pool.server(exclude=self.excludeservers)

            # Set kind of server in DataFrame
            current_message.append(kind)

            # add the open request to the collection of open servers, so
            # we can release it later on
            current_message.append(server)

            # attempt to parse a server request
            try:

                # check if there's a server available
                if not server:
                    raise Exception("SERVER UNAVAILABLE")

                # set used server in route
                route.append(server.state())

                # ask the server for a new request at
                request = server.request()

                # Add request to list of open open_requests
                current_message.append(request)

                request_df.loc[idx] = current_message

                # Define message to server
                sent_message = self._env.process(self.server_message(
                    process_id, requested_by, request, server))

                # send a message and wait for message or timeout to complete
                yield sent_message | self._env.timeout(self._timeout)

                # If message not triggered then timeout is past
                if (not sent_message.triggered):
                    sent_message.interrupt("TIMEOUT")

                # When request is processed and return loop index exists
                # Release in between servers
                if return_loop:

                    # release all server requests between occurances of the same kind
                    for row in request_df.loc[return_loop[0]:idx].itertuples(index=False):

                        # Get server and corresponding request
                        server = getattr(row, "open_servers")
                        request = getattr(row, "open_requests")

                        # release the server request
                        if server and request:
                            # Only release if request is still linked to server
                            if request in server.users:
                                server.release(request=request)

                    # remove closed request from DataFrame
                    request_df = request_df.drop(range(return_loop[0], idx), axis=0)

            # handle exceptions
            except Exception as e:
                print(e)
                break
                # log to the error log
                self._env.log(
                    f"{self._env.now};;ERROR;;;;{process_id};{requested_by['name']};Error due to {e}", level=40)

        # release all server requests when entire loop is done
        for row in request_df.itertuples(index=False):

            # Get server and corresponding request
            server = getattr(row, "open_servers")
            request = getattr(row, "open_requests")

            # release the server request
            if server and request:
                server.release(request=request)

    def server_message(self, process_id, requested_by, request, server):
        start = self._env.now
        try:
            # yield the request and timeout
            yield request
            # Get server state with current load
            server_state = server.state()
            yield self._env.timeout(server_state['latency'])

            # we need to construct a logmessage
            # and push onto the environment
            message = f"Requesting {server_state['name']} by {requested_by['name']}"
            self._env.log(
                f"{self._env.now};{server_state['name']};INFO;{server_state['cpu']};{server_state['memory']};{server_state['latency']};{process_id};{requested_by['name']};{message}")

        # handle interruptions
        except Interrupt as interrupt:
            server_state = server.state()

            # Check if error is due to interuption using error_generator
            if isinstance(interrupt.cause, Preempted):

                # Manually print timeout message
                self._env.log(
                    f"{self._env.now};{server_state['name']};ERROR;{server_state['cpu']};{server_state['memory']};{server_state['latency']};{process_id};{requested_by['name']};Error due to TIMEOUT at time {start + self._timeout}", level=40)
            else:

                # Use interrupt clause to write error message
                self._env.log(
                    f"{self._env.now};{server_state['name']};ERROR;{server_state['cpu']};{server_state['memory']};{server_state['latency']};{process_id};{requested_by['name']};Error due to {interrupt.cause}", level=40)
