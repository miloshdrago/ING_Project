/**
 *  Main function loop for the webclient code.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   static/main.js
 *  @scope  public
 */

// strict checks
'use strict';

// dependencies
import { Forms } from './js/Forms.js';
import { api } from './js/Api.js';

/**
 *  Event handler that initialized when the document
 *  is ready.
 */
onload = function() {

    /**
     *  Element for encapsulating the main content of
     *  the webclient. This will hold all subsequently
     *  created classes and such.
     *  @var    Element
     */
    const mainContainer = document.getElementById('main');


    /**
     *  Form for starting a simulation.
     */
    Forms.create(mainContainer, '/simulation.json', {
        className: 'simulation-form'
    }).then((form) => {

        /**
         *  Listener for the submit event on the form, so we know when
         *  to start a new simulation, and parse the data before sending
         *  it to the api.
         */
        form.on('submit', (e) => {

            console.log(form)
            /**
             *  Data to post to the api as formdata.
             *  @var    FormData
             */
            const formdata = new FormData();

            // append all data entries to the formdata
            Object.entries(form.data()).forEach(([k, v]) => formdata.set(k, v));

            /**
             *  Post request to startup a new simulation based on the
             *  values of the form.
             *  @var    Promise
             */
            console.log(formdata)
            api.post('/simulation', formdata).then((res) => {

                // test output
                console.log(res);
                

            });

            // console.log(simID)
            // Redirect to '/' with corresponding logfile (parameter f)
            // window.location.href = "/?f=Manual_Log.csv#Visualisation";

        });
    });
};


