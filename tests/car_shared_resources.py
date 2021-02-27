#!/usr/bin/env python3

# dependencies
import unittest
import simpy

def car(env, name, bcs, driving_time, charge_duration):
    """Generator function to act as car process for a simpy simulation"""

    # simulate driving to the station (bcs)
    yield env.timeout(driving_time)

    # we need to request a charging point
    print("%s arriving at %d" % (name, env.now))

    # open a new context with the request, so it gets released after
    # the request has finished. otherwise call `release()`
    with bcs.request() as req:

        # we need to yield the request to let others know this resource is taken
        yield req

        # we need to charge the battery
        print("%s starting to charge at %d" % (name, env.now))
        yield env.timeout(charge_duration)
        print("%s leaving battery charging station at %d" % (name, env.now))


class CarTestCase(unittest.TestCase):
    """Class as test case for the car process"""

    def test_car_process(self):
        """Test for the car process"""

        # we need an env
        env = simpy.Environment()

        # we need a new resource for the battery charging station.
        # we allow two cars to charge
        bcs = simpy.Resource(env, capacity=2)

        # add a number of cars that want to drive and charge
        for n in range(4):
            env.process(car(env, "Car %d"%n, bcs, n*2, 5))

        # run a simulation
        env.run()

# run all test cases
if __name__ == "__main__":
    unittest.main()