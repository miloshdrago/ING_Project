"""
Class for creating an environment where a simulation can run in.
This is a small extension of the simpy.Environment which allows
us to add some additional middleware functionality.

@file   lib/Environment.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  public
"""

# dependencies
import simpy


class Environment(simpy.Environment):

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """

        # call the parent class
        super().__init__(*args, **kwargs)

        # collection of loggers
        self._loggers = {"info": [], "error": []}

        # collection of middlewares
        self._middleware = []

    def log(self, message, level=20, type="info"):
        """
        Method to log a message to the environment.

        Parameters
        ----------
        type: string
            Type of log message. Supported types are:
            - info:     Regular info messages.
            - error:    Error messages.
        message: string
            Message to log.

        Returns
        -------
        self
        """

        # log the message on all loggers of the given type
        [Logger.log(message, level) for Logger in self._loggers[type]]

        # allow chaining
        return self

    def logger(self, Logger, type="info"):
        """
        Method to install a logger for a specific type of log on this environment.

        Parameters
        ----------
        type: string
            Type of logger. Supported types are:
            - info:     Regular info logger.
            - error:    Error logger.
        Logger: Logger
            Logger instance that will log those messages.

        Returns
        -------
        self
        """

        # install the logger
        self._loggers[type].append(Logger)

        # allow chaining
        return self

    def use(self, middleware):
        """
        Method to install middleware on this environment.

        Parameters
        ----------
        middleware: Middleware
            The middelware to install.

        Returns
        -------
        self
        """

        # install the middleware
        self._middleware.append(middleware)

        # allow chaining
        return self

    def push(self, message):
        """
        Method to forcibly push a message through the pipeline of
        the environment's simulation. This is the opposite of
        the "pull" wrapper around the step method.

        Parameters
        ----------
        message: string
            Message to pipe through this environment.

        Returns
        -------
        self
        """

        # iterate over all middlewares to push the messages
        for m in self._middleware:

            # only pipe valid message
            if m:
                m.pipe(message)

        # allow chaining
        return self

    def step(self):
        """
        Method that wraps around simpy.Environment.step.
        """
        # we need the current process, which we can pipe
        # to our middleware
        current = self.active_process

        # we need to iterate over the middleware, so we
        # can pipe the active process to that
        for m in self._middleware:

            # only pipe valid message
            if m:
                m.pipe(current)

        # call the original method
        return super().step()
