"""
Class for exposing the default interface of middleware. This class should never
be instantiated. This class can be inherited if you want to create your
own middleware, which can be used by a simulation.

@file   lib/Middleware.py
@author Tycho Atsma <tycho.atsma@gmail.com>
@scope  private
"""

# dependencies
from abc import ABCMeta, abstractmethod
import unittest

class Middleware(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        """
        Constructor.
        """
        pass

    @abstractmethod
    def pipe(self, message):
        """
        Abstract method to pipe a message through your custom
        middleware handling.

        Parameters
        ----------
        message: string
            Message to pipe through this middleware.

        Returns
        -------
        self
        """
        pass

class MiddlewareTestCase(unittest.TestCase):

    def test_should_not_construct(self):
        """
        Test to ensure that the class cannot be instantiated.
        """
        self.assertRaises(TypeError, Middleware)

# run as main
if __name__ == "__main__":
    unittest.main()
