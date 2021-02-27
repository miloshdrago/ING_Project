"""
Toy example on how to report a timeout when a certain time is past
"""

from random import randint
import simpy

error_time = 30


def message(env, i):
    # Enter all message processes here, for now random timeout
    try:
        process_time = randint(25, 35)
        yield env.timeout(process_time)
        print(f"INFO: message {i} processed at time {env.now}, duration {process_time}")
    except simpy.Interrupt as interrupt:
        print(f"ERROR: message {i} {interrupt.cause} at time {env.now}")


def message_generator(env):
    for i in range(10):

        message_process = env.process(message(env, i))
        yield message_process | env.timeout(error_time)

        # If message not triggered then timeout is past
        if (not message_process.triggered):
            message_process.interrupt("timeout")


if __name__ == "__main__":
    env = simpy.Environment()
    env.process(message_generator(env))
    env.run(until=240)
