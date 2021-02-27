/**
 *  Class mixin for implementing an interface for triggering and listening to
 *  events on an instance of this mixin.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/EventBus.js
 *  @scope  public
 */

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const events = Symbol('events');

/**
 *  Mixin for applying an eventbus interface.
 *  @param  class   Class to mixin with.
 *  @return class
 */
export const EventBus = (superclass) => class extends superclass {

    /**
     *  Constructor.
     */
    constructor(...args) {

        // call the parent class
        super(...args);

        /**
         *  Collection of events.
         *  @var    Object
         */
        this[events] = { };
    }

    /**
     *  Method to install an event listener.
     *  @param  String      Name of the event.
     *  @param  Function    Listener callback.
     *  @return this
     */
    on(eventName, listener) {

        // we need a new collection of listeners
        if (!this[events][eventName]) this[events][eventName] = [];

        // add the listener to the collection
        this[events][eventName].push(listener);

        // allow chaining
        return this;
    }

    /**
     *  Method to uninstall an event listener.
     *  @param  String              Name of the event.
     *  @param  Function|undefined  Optional listener to uninstall explicitely.
     *  @return this
     */
    off(eventName, listener) {

        // we need a collection of listeners
        if (!this[events][eventName]) return this;

        // we need to uninstall all events if no explicit listener needs to
        // be uninstalled
        if (!listener) {

            // drop all listeners
            this[events][eventName].length = 0;

            // drop the reference
            delete this[events][eventName];
        }

        // otherwise, we need to find the right listener
        else {

            // which we need to iterate over the collection of listeners for
            this[events][eventName].forEach((func, idx) => {

                // drop the reference to the listener if it's the same
                if (func == listener) this[events][eventName].splice(idx, 1);
            });
        }

        // allow chaining
        return this;
    }

    /**
     *  Method to trigger an event.
     *  @param  String  Name of the event.
     *  @param  any     Data to pass along with the event (Object is recommended).
     *  @return this
     */
    trigger(eventName, data) {

        // we need a collection of listeners
        if (!this[events][eventName]) return this;

        // we need to iterate over all listeners and call them
        this[events][eventName].forEach((listener) => listener(data));

        // allow chaining
        return this;
    }

    /**
     *  Cleanup.
     */
    remove() {

        // drop all references to the events
        this[events] = null;
    }
};
