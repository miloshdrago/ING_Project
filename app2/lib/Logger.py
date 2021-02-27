"""
Class for logging. This class can be used for logging processes that
occur within a simulation given a certain level. This can be installed
a middleware on a simulation.

@file   lib/Logger.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from lib.Middleware import Middleware
import logging
import os
from logging.handlers import QueueHandler, QueueListener
import queue

# get location log files relative to this file
LOG_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logs'))


class Logger(Middleware):

    def __init__(self, name, directory=LOG_PATH, show_stdout=True, usequeue=False):
        """
        Constructor.

        Parameters
        ----------
        name: string
            Name of the file that content will be logged to.
        directory: string
            Path to a directory where all logfiles should be written
            to. Note that this directory must exist before logging.

        Throws
        ------
        ValueError
            Is raised when the directory does not exist.
        """
        # we need to check if the given directory path actually
        # points to an existing directory, otherwise we stop
        if not os.path.isdir(os.path.join(directory)):
            raise ValueError("directory does not exist")

        # we need to get the logger with the given name
        self._logger = logging.getLogger(name)

        if not show_stdout:
            # Do not propagate to higer level to keep message out of stout
            self._logger.propagate = False

        # we need a new file handler so the logs are written to the file
        filehandler = logging.FileHandler(os.path.join(directory, name+".csv"), mode='a')

        if usequeue:
            log_queue = queue.Queue(-1)
            queue_handler = QueueHandler(log_queue)
            self._logger.addHandler(queue_handler)
            self.listener = QueueListener(log_queue, filehandler)

        else:
            # add the file handler to the logger so all logs will be outputted there
            self._logger.addHandler(filehandler)

        # assign the directory
        self._directory = directory

    def log(self, message, level=20):
        """
        Method to log a message.

        Parameters
        ----------
        message: string
            Message to log.
        level: integer
            Level of logging (default: 20).

        Returns
        -------
        self
        """

        # log the message using our logger
        self._logger.log(level, message)

        # allow chaining
        return self

    def pipe(self, message):
        """
        Method to pipe a message to this logger.

        Parameters
        ----------
        message: string
            Message to pipe through this logger.

        Returns
        -------
        self
        """

        # log the message
        if message:
            self.log(message)

        # allow chaining
        return self
