#!/usr/bin/env python3
"""
Script to run the simulation as CLI tool.

@file   command_line_simulation.py
"""

# dependencies
from lib.Environment import Environment
from lib.MultiServers import MultiServers
from lib.Servers import Servers
from lib.Logger import Logger
from lib.MessageGenerator import MessageGenerator
from lib.ErrorGenerator import ErrorGenerator
from lib.Seasonality import TransactionInterval as Seasonality

# 3rd party dependencies
import os
import glob
from datetime import datetime
import json
from argparse import ArgumentParser, RawTextHelpFormatter

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
import logging
logging.basicConfig(level=logging.INFO)


def parse_args():
    "Parses inputs from commandline and returns them as a Namespace object."

    parser = ArgumentParser(prog='command_line_simulation.py',
                            formatter_class=RawTextHelpFormatter,
                            description=' Runs Simpy simulation from command line.')
    parser.add_argument('-c', '--config',
                        help='path to a json formatted configuration file')

    return parser.parse_args()


def main(n, config, seasonality, log_dir, log_prefix, description):
    """
    Main loop that runs a simulation. This simulation can be configured by passing
    a configuration dictionary, and specifying where all logs will be written to.

    Parameters
    ----------
    n: int
        The Nth simulation.
    config: dict
        Configuration for the simulation. Should contain the following keys:
        - servers:      List of dictionaries, describing a server pool.
        - process:      Sequence of kinds of servers, describing how a process within
                        the simulation runs.
        - runtime:      Until when the simulation should run.
        - max_volumne:  Maximum number of events.
    seasonality: Seasonality
        Seasonality object to use for the simulation. This defines the intervals
        between events.
    log_dir: string
        Path pointing to where all logs should be written.
    log_prefix: string
        Prefix of every log file.

    Returns
    -------
    bool
    """
    # we need a new environment which we can run.
    environment = Environment()

    # we need a server pool
    servers = MultiServers()

    # iterate over all of the servers that need to be configured that
    # we received from the client
    for server in config['servers']:

        # append a new server pool to the multiserver system
        servers.append(
            Servers(environment, size=server['size'], capacity=server['capacity'], kind=server['kind']))

    # we need a logger that will log all events that happen in the simulation
    name = "{0}_{1:04d}_{2}_{3}".format(log_prefix, n,
                                        datetime.now().strftime("%Y-%m-%d_%H-%M"),
                                        description.replace(" ", "-"))
    logger = Logger(name, directory=log_dir, show_stdout=False, usequeue=False)

    # we also need a logger for all error events that happen in the simulation
    error_logger = Logger(f"error-{name}", directory=log_dir, show_stdout=False)

    # Start QueueListener
    if hasattr(logger, "listener"):
        logger.listener.start()

    # Enter first line for correct .csv headers
    logger.log(
        'Time;Server;Message_type;CPU Usage;Memory Usage;Latency;Transaction_ID;From_Server;Message')
    error_logger.log('Time;Server;Error type;Start-Stop')

    # we can use the logger for the simulation, so we know where all logs will be written
    environment.logger(logger)
    environment.logger(error_logger, type="error")

    # we need a new form of seasonality
    seasonality = Seasonality(seasonality, enviroment=environment, max_volume=config["max_volume"])

    # now, we can attach the MessageGenerator to the simulation envoirment
    for proc in config['process']:
        MessageGenerator(environment, servers, seasonality, kinds=proc, timeout=config['timeout'])

    # Add error generator if specified
    if 'error' in config:
        print("With error function")
        ErrorGenerator(environment, servers, config['error']['errorwait'],
                       config['error']['error_duration'])

    # run the simulation with a certain runtime (runtime). this runtime is not equivalent
    # to the current time (measurements). this should be the seasonality of the system.
    # for example, day or week.
    environment.run(until=int(config['runtime']))

    # Start QueueListener
    if hasattr(logger, "listener"):
        logger.listener.stop()

    return name


# run this as main
if __name__ == "__main__":
    # For timing get current time
    starttime = datetime.now()

    # Find directory of this file
    file_dir = os.path.dirname(os.path.abspath(__file__))

    args = parse_args()
    # if hasattr(args, "config") & args.config is not None:
    if args.config is not None:
        config_file = args.config
        print("Loaded config file: ", config_file)

    else:
        # Load standard config file
        config_file = os.path.join(file_dir, 'config.json')
        print("Standard config file: ", config_file)

    # configuration for the simulation to run
    with open(config_file) as f:
        config = json.load(f)

    # log_dir = os.path.join(file_dir, "CLI_Logs")
    log_dir = os.path.join(file_dir, "Logs")
    seasonality = os.path.join(file_dir, 'seasonality', 'week.csv')
    log_prefix = "log"

    # get simulation count by counting number of simulation files in folder
    n = len(glob.glob(os.path.join(log_dir, log_prefix+'*'))) + 1

    # run main
    location_file = main(n=n, config=config, seasonality=seasonality,
                         log_dir=log_dir, log_prefix=log_prefix,
                         description=config['description'])
    print(f"Simulation is done and can be found at {os.path.join(log_dir,location_file)}.")
    print(f"Total time {datetime.now() - starttime}")
