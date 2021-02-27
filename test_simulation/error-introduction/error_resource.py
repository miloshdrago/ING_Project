"""
Toy example on how introduce error using PreemptiveResource
"""

from random import uniform

import simpy

timeout_time = 0.5
error_duration = (3, 5)
inter_transaction_time = (.01, 0.1)
errorwait = (2, 5)
runtime = 10


def message(env, server, i):
    # Enter all message processes here, for now random timeout
    try:
        process_time = uniform(inter_transaction_time[0], inter_transaction_time[1])
        with server.request(priority=1) as req:  # Generate a request event
            yield req                    # Wait for access
            yield env.timeout(process_time)
        print(f"INFO: message {i} processed at time {env.now}, duration {process_time}")
    except simpy.Interrupt as interrupt:
        # Check if error is due to interuption using error_generator
        if isinstance(interrupt.cause, simpy.resources.resource.Preempted):
            # Manually print timeout message
            print(f"ERROR: message {i} timeout at time {env.now}")
        else:
            # Use interrupt clause to write error message
            print(f"ERROR: message {i} {interrupt.cause} at time {env.now}")


def message_generator(env, server):
    for i in range(1000):

        message_process = env.process(message(env, server, i))
        yield message_process | env.timeout(timeout_time)

        # If message not triggered then timeout is past
        if (not message_process.triggered):
            message_process.interrupt("timeout")


def error_generator(env, server):
    while True:
        # Wait a random amount of time to introduce the error
        yield env.timeout(uniform(*errorwait))
        print(f"LOG_ERROR_Start error at time {env.now}")
        # Make an equal amount of requests to the capacity of the server
        # Make a list of requests
        request_list = [server.request(priority=0) for i in range(server.capacity)]
        for request in request_list:
            yield request  # Send priority request to PreemptiveResource
        # Wait for the error to be resolved
        yield env.timeout(uniform(*error_duration))
        # Release spots in server when the error is resolved
        for request in request_list:
            yield server.release(request)
        print(f"LOG_ERROR_End error at time {env.now}")


if __name__ == "__main__":
    env = simpy.Environment()
    serv = simpy.PreemptiveResource(env, capacity=5)
    env.process(error_generator(env, serv))
    env.process(message_generator(env, serv))
    env.run(until=runtime)
