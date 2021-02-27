#!/usr/bin/env python3

# dependencies
import unittest
import simpy

class Car(object):
    """
    Class for simulating a car process.
    """

    def __init__(self, env):
        """
        Constructor.

        Parameters
        ----------
        env : simpy.Environment
            Environment to run the process in.
        """
        self.env = env

        # run this process immediately
        self.process = self.env.process(self.run())

    def run(self):
        """
        Generator method to run as simpy process.

        Yields
        ------
        simpy.Timeout or simpy.Process
        """
        while True:
            print("Start parking and charging a car at %ds" % self.env.now)
            charge_duration = 5
            
            # try charging a car
            try:
                # yield a new process for charging a car
                yield self.env.process(self.charge(charge_duration))

            # charging a car can be interrupted
            except simpy.Interrupt as e:

                # we stop charging a car, and drive instead
                print("Stop charging a car at %ds" % self.env.now)

            print("Start driving a car at %ds" % self.env.now)
            drive_duration = 3

            # yield a new timeout for driving a car
            yield self.env.timeout(drive_duration)

    def charge(self, duration):
        """
        Generator method to create a new simpy timeout to simulate
        the charging of a car.
        
        Yields
        ------
        simpy.Timeout
        """
        yield self.env.timeout(duration)

class CarTestCase(unittest.TestCase):
    """
    Test case for interacting with simpy Processes. This is done
    through the use of the test Car class.

    The example tests are based on the introduction on
    the documentation of simpy: https://simpy.readthedocs.io/en/latest/simpy_intro/basic_concepts.html.
    """

    def test_car_process(self):
        """
        Test for running the car process through an object interface.
        """
        env = simpy.Environment()

        # we need a new car
        car = Car(env)

        # run a simulation with a car process until simulated 20 seconds
        env.run(until=20)

    def test_drive_interrupt(self):
        """
        Test for running the car process and interrupting it with a driver.
        """
        env = simpy.Environment()

        # we need a new car
        car = Car(env)

        def driver(env, car):
            """Process of a driver"""

            # driver can only wait three seconds
            yield env.timeout(3)

            # interrupt the car after those three seconds
            car.process.interrupt()

        # add a driver as process
        env.process(driver(env, car))

        # run a simulation for 20 simulated seconds
        env.run(until=20)

# run all test cases
if __name__ == "__main__":
    unittest.main()
