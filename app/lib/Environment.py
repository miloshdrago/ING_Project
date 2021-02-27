"""
Class for creating an environment where a simulation can run in.
This is a small extension of the simpy.Environment which allows
us to add some additional logging functionality.

@file   lib/Environment.py
@author Tycho Atsma <tycho.atsma@gmail.com>
        Joris van der Vorst <joris@jvandervorst.nl>
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
