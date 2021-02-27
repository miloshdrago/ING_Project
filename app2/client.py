#!/usr/bin/env python3
"""
Class for starting up a webclient, which can be used as frontend for the
simulation.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   client.py
@scope  public
"""

# 3rd party dependencies
from flask import Flask
from dash import Dash
import dash
import dash_html_components as html
import webbrowser
from threading import Timer

# dependencies
import routes

class Client(object):

    def __init__(self, config):
        """
        Constructor.

        Parameters
        ----------
        config: dict
            Configuration for the flask application.
        """
        # we need to construct a flask application, which will be the
        # backbone of the web client
        self._client = Flask(__name__, 
                            static_url_path='', 
                            static_folder="web/static", 
                            template_folder="web/templates"
                            )

        # Dash app
        self._dashapp = Dash(__name__, 
                            server=self._client, 
                            routes_pathname_prefix='/dash/', 
                            external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
                            )

        # Launch Dash app
        self._dashapp.layout = html.Div(children=[
            html.H6(children='Dash app successfully launched.'),
        ])

        # we need to setup some configuration variables, these may need to change
        # when running in production
        self._client.config.update(config)

        # we need to install all routes onto the client
        routes.install(self._client, self._dashapp)

    def run(self):
        """
        Method to run the client. This will start up a simple webserver.
        """
        # run the dash application
        self._dashapp.run_server(debug=True)
        


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')


# run as main
if __name__ == "__main__":

    # Timer(1, open_browser).start();

    # run a new client
    Client({
        'TESTING':  True,
        'ENV':     'development',
        'DEBUG':    True
    }).run()


