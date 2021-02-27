/**
 *  Class for making api requests. This class can be used as static interface,
 *  or dynamic, by setting a prefix upon construction.
 *
 *  Currently, only GET and POST requests are supported, as there is no need
 *  for anything else (yet).
 *
 *  All supported data types are defined here: "https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/fetch".
 *
 *  @example    ```
 *              import { Api, api } from './path/to/Api.js';
 *
 *              // static calling
 *              api.post('/simulation', formdata);
 *              api.get('/simulation', { id: 1 });
 *              
 *              // dynamic calling
 *              const endpoint = new Api('/simulation');
 *              endpoint.post(formdata);
 *              endpoint.get({ id: 1 });
 *              ```
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Api.js
 *  @scope  public
 */

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const prefix = Symbol('prefix');

/**
 *  Export class definition.
 */
export class Api {

    /**
     *  Constructor.
     *  @param  String  (Optional) Prefixed endpoint.
     */
    constructor(_prefix = '') {

        /**
         *  Prefix of all endpoints.
         *  @var    String
         */
        this[prefix] = _prefix;
    }

    /**
     *  Method to make a GET request.
     *  @param  String|mixed    Endpoint or data.
     *  @param  mixed|undefined (Optional) data.
     *  @return Promise
     */
    get(urlOrData, data) {

        // determine the prefix
        const pre = this[prefix] || '';

        // we need an endpoint to make a request to
        const endpoint = data ? pre + urlOrData : pre;

        // we need a payload to send with the request
        const payload = data || urlOrData;

        // we need to convert the data object to url params, as the get request
        // does not accept a body
        const params = new URLSearchParams(payload);

        // make a new get request with the endpoint and payload
        return fetch(`${endpoint}?${params}`, {
            method: "GET",
        }).then((response) => response.json());
    }

    /**
     *  Method to make a POST request.
     *  @param  String|mixed    Endpoint or data.
     *  @param  mixed|undefined (Optional) data.
     *  @return Promise
     */
    post(urlOrData, data) {

        // determine the prefix
        const pre = this[prefix] || '';

        // we need an endpoint to make a request to
        const endpoint = data ? pre + urlOrData : pre;

        // we need a payload to send with the request
        const payload = data || urlOrData;

        // make a new get request with the endpoint and payload
        return fetch(endpoint, {
            method: "POST",
            body:   payload
        }).then((response) => response.json());
    }
};

/**
 *  Export "static class", to act as singleton main api class.
 */
export const api = new Api();
