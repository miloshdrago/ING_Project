#!/usr/bin/env python3

# dependencies
import unittest
import simpy

class SimpyTestCase(unittest.TestCase):
    """
    Test case for running simpy. This test case only
    demonstrates simply concepts of simpy and if
    they work.

    The example tests are based on the introduction on
    the documentation of simpy: https://simpy.readthedocs.io/en/latest/simpy_intro/basic_concepts.html.
    """

    def test_run_simpy(self):
        """
        Method to test if simpy runs.
        """
        env = simpy.Environment()
        env.run()

    def test_run_car_process(self):
        """
        Method to test if a simpy process runs as expected.
        """
        env = simpy.Environment()
        
        # we need a new process
        def process_car(env):
            while True:

                # park the car
                print("Start park duration %d" % env.now)
                parking_duration = 5
                yield env.timeout(parking_duration)

                # drive the car
                print("Start trip duration %d" % env.now)
                trip_duration = 3
                yield env.timeout(trip_duration)

        # we need to tell the environment about the car process
        env.process(process_car(env))

        # run the car process until (simulated) 20 seconds
        env.run(until=20)

# run all test cases
if __name__ == "__main__":
    unittest.main()
