"""
This file contains a function that installs a number of routes on a flask
webclient. This is more of a collection of routes than an actual function,
but this method allows us to easily call it from other places and keep that
part clean from these declarations.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   routes.py
@scope  public
"""

# third party dependencies
from lib.LogProcessing import show_dash_graphs
from lib.Logger import Logger
from lib.Processor import Processor
from lib.LogProcessing import get_endpoint_json, show_dash_graphs
from lib.Seasonality import TransactionInterval as Seasonality
from lib.Servers import Servers
from lib.MultiServers import MultiServers
from lib.Environment import Environment
import os
from os.path import isfile, join, normpath, dirname, basename, getctime, exists
from flask import request, render_template, send_file
from flask.json import jsonify, load
from datetime import datetime
import time
import requests 
import zipfile
import io
import pathlib
import glob
from uuid import uuid4

# we need to setup logging configuration here,
# so all other loggers will properly function
# and behave the same
import logging
logging.basicConfig(level=logging.INFO)

# dependencies

# GLOBALS
LOG_PATH = normpath(join(dirname(__file__), 'logs'))
Seasonality_folder = normpath(join(dirname(__file__), 'seasonality'))
Seasonality_file = 'week.csv'
file_prefix = "log"


def install(client, dashapp):
    """
    Function to install all routes onto a flask webclient.

    Parameters
    ----------
    client: Flask
        Flask application to install the routes on.
    """

    # global simulation count
    simc = len(glob.glob(os.path.join(LOG_PATH, file_prefix+'*')))

    # declare the index route
    @client.route('/')
    def index():
        """
        Function to generate and expose content for the index route.

        Returns
        -------
        string
        """

        # Scan the logfile directory
        list_of_files = glob.glob(join(LOG_PATH, 'log_*.csv'))

        # Return only the filename to get no errors with old functions
        log_filenames = [basename(filename) for filename in list_of_files]

        if log_filenames and 'f' in request.args:
            # Parse URL request file f using last_created default
            f = request.args.get('f')

            # api-endpoint 
            URL = "http://127.0.0.1:8050/generate-dash-graph"
              
            # defining a params dict for the parameters to be sent to the API 
            PARAMS = {'f': f} 
              
            # sending get request and saving the response as response object 
            r = requests.get(url = URL, params = PARAMS) 
              
            # extracting data in json format 
            data = r.json() 

            # Wait for the Dash app to update its layout before returning front-end index.html (this is a critical line)
            time.sleep(3)

            return render_template('index.html', log_filenames=log_filenames, len_logfiles=len(log_filenames), f=f)

        elif log_filenames:
            return render_template('index.html', log_filenames=log_filenames, len_logfiles=len(log_filenames), f='')

        else:
            print("No logfiles were found in /logs. Please run a simulation first.")
            return render_template('index.html', log_filenames=[], len_logfiles=0, f='')

    # declare endpoint for retrieving forms
    @client.route('/forms/<name>')
    def forms(name):
        """
        Function to install handlers on the /forms path. This allows for
        retrieving predefined forms.

        Parameters
        ----------
        GET:
            name: string
                Name of the form file.

        Returns
        -------
        GET: string
        """
        # construct the path to the form
        fp = join(dirname(__file__), 'web', 'forms', name)

        # we need to have a valid path
        if not exists(fp):

            # tell the user there's no form
            return jsonify({"error": "file does not exist"})

        # open the file
        with open(fp) as form:

            # expose the json of the form
            return load(form)

    # declare endpoint for starting a new simulation
    @client.route('/simulation', methods=["GET", "POST"])
    def simulation():
        """
        Function to install handlers on the /simulation path. This allows for
        requesting simulation data or starting a new simulation.

        Parameters
        ----------
        POST:

            servers: list
                List containing configurations for a server pool as dicts.
                { capacity: int, size: int, kind: string }
                For example, { size: 10, capacity: 10, kind: 'regular' }.

            process: list
                List specifying how a process should go (from server to server).
                This should contain a sequence of server kinds.
                For example, ["regular", "balance", "pay"].

            runtime: int
                Runtime of the simulation (defined by simpy package).

        Returns
        -------
        GET: dict
        POST: int
        """
        if request.method == "POST":

            # nonlocal use of the simulation count
            nonlocal simc

            # increment the simulation count
            simc += 1

            # we need a new environment which we can run.
            environment = Environment()

            # we need a server pool
            servers = MultiServers()

            # iterate over all of the servers that need to be configured that
            # we received from the client
            for kind in request.form['kinds'].split(','):

                # append a new server pool to the multiserver system
                servers.append(Servers(environment, size=int(request.form['size']), capacity=int(
                    request.form['capacity']), kind=kind.strip()))

            # Get the current date and time to append to the logger file name
            log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

            # now that we have an output dir, we can construct our logger which
            # we can use for the simulation
            name = "{0}_{1:04d}_{2}".format(file_prefix, simc, log_timestamp)
            logger = Logger(name, directory=LOG_PATH)

            # we also need a logger for all error events that happen in the simulation
            error_logger = Logger(f"error-{name}", directory=LOG_PATH)

            # Enter first line for correct .csv headers
            logger.info(
                'Time;Server;Message_type;CPU Usage;Memory Usage;Latency;Transaction_ID;To_Server;Message')
            error_logger.info('Time;Server;Error type;Start-Stop')

            # we can use the logger for the simulation, so we know where all logs will be written
            environment.logger(logger)
            environment.logger(error_logger, type="error")

            # we need a new form of seasonality
            seasonality = Seasonality(join(Seasonality_folder, Seasonality_file),
                                      max_volume=int(request.form['max_volume']))

            # now, we can put the process in the simulation
            Processor(environment, servers, seasonality=seasonality, kinds=[
                      kind.strip() for kind in request.form['process'].split(',')])

            # run the simulation with a certain runtime (runtime). this runtime is not equivalent
            # to the current time (measurements). this should be the seasonality of the system.
            # for example, day or week.
            environment.run(until=int(request.form['runtime']))

            # expose the id of the simulation
            return jsonify(simc)

        if request.method == "GET":

            if 'id' in request.args:
                logfile_id = "{:04d}".format(int(request.args.get('id')))

            # Scan the logfile directory
            list_of_files = glob.glob(os.path.join(LOG_PATH, 'log_*.csv'))

            # Return only the filename to get no errors with old functions
            log_filenames = [os.path.basename(filename) for filename in list_of_files]

            if log_filenames:

                logfile_ids = [f.split('_')[1] for f in log_filenames]
                name_id_dict = dict(zip(logfile_ids, log_filenames))

                if logfile_id in logfile_ids:
                    # Logfile associated to given ID was successfully found
                    return jsonify({"data": name_id_dict[logfile_id], "message": "success"})

                else:
                    # No logfile associated to given ID was found
                    return jsonify({"message": "No logfile (.csv) with given ID exists."})
            else:
                # No logfiles found (/logs is empty)
                return jsonify({"message": "No logfiles were found in /logs."})



    @client.route('/get_endpoint_data')
    def get_endpoint_data():
        """
        Function to process the .csv logfile and return an endpoint_matrix
        in JSON format.

        Parameters
        ----------
        f: logfile name

        Returns
        -------
        GET: JSON
        """

        # Scan the logfile directory
        list_of_files = glob.glob(join(LOG_PATH, 'log_*.csv'))

        # Return only the filename to get no errors with old functions
        log_filenames = [basename(filename) for filename in list_of_files]

        # Only process/return endpoint_matrix if a logfile exists
        if log_filenames:

            last_created = basename(max(list_of_files,
                                        key=getctime))

            # Parse URL request file f using last_created default
            f = request.args.get('f', default=last_created)

            return get_endpoint_json(f)
            
        else:
            json_convert = {"data": 0, "message": "No logfile found."}
            return jsonify(json_convert)



    @client.route('/download-logs')
    def download_logfile():
        """
        Function to zip and download logfiles in /logs.

        Returns
        -------
        GET: .zip file (download)
        """

        base_path = pathlib.Path(LOG_PATH)
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for f_name in base_path.iterdir():
                z.write(f_name)

        data.seek(0)

        return send_file(
            data,
            mimetype='application/zip',
            as_attachment=True,
            attachment_filename='logs.zip'
        )



    @client.route('/generate-dash-graph')
    def generate_dash_graph():
        """
        Function to generate dash graphs for a given logfile

        Returns
        -------
        GET: Success/Failure message (JSON)
        """

        if 'f' in request.args:
            f = request.args.get('f')
            eventId = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

            show_dash_graphs(dashapp, f, eventId)

            return ({"message": "Dash graphs successfully generated."})

        else:
            return jsonify({"message": "No logfile parameter (f) was given in the request."})

