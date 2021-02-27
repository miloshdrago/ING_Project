/**
 *  Class for managing classes that are instantiated on an element.
 *  This takes care of the obnoxious bookkeeping of classes as
 *  a collection, and cleaning them up after a certain process.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Container.js
 *  @scope  public
 */

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');
const instances = Symbol('instances');

/**
 *  Export class definition.
 */
export class Container {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for the container. Supported options are:
     *                  
     *                      "className" String  Additional css class(es).
     *                      "element"   String  Type of element (e.g. div).
     */
    constructor(parent, config = {}) {

        /**
         *  Default configuration.
         *  @var    Object
         */
        config = Object.assign({
            element: 'div'
        }, config);

        /**
         *  Element for encapsulating all classes.
         *  @var    Element
         */
        this[container] = parent.appendChild(document.createElement(config.element));

        /**
         *  Collection of instances of appended classes.
         *  @var    Array
         */
        this[instances] = [];

        // add additional css classes
        if (config.className) this[container].classList.add(config.className);
    }

    /**
     *  Getter method to expose all installed instances.
     *  @return Array
     */
    get installed() {

        // expose a copy of the list of instances
        return Array.from(this[instances]);
    }

    /**
     *  Method to append classes to the container.
     *  @param  Function    Constructor function of the class. Should accept
     *                      a parent element as first parameter.
     *  @param  variadic    Additional arguments for the constructor.
     *  @return mixed
     */
    append(Constructor, ...args) {

        // construct a new instance
        const instance = new Constructor(this[container], ...args);

        // remember this instance
        this[instances].push(instance);

        // decorate the instance remove method so it also gets removed from
        // the collection of instances
        if (instance.remove) instance.remove = ((remove) => () => {

            // we need the index of the instance in the collection, so we can
            // remove the correct one
            const index = this[instances].indexOf(instance);

            // remove from the collection
            if (~index) this[instances].splice(index, 1);

            // call the original remove method
            if (remove instanceof Function) remove();
        })(instance.remove.bind(instance));

        // expose the instance
        return instance;
    }

    /**
     *  Method to set a class on the container. This will overwrite everything
     *  that has been set or appended before.
     *  @param  Function    Constructor function of the class. Should accept
     *                      a parent element as first parameter.
     *  @param  variadic    Additional arguments for the constructor.
     *  @return mixed
     */
    set(Constructor, ...args) {

        // clear the container
        this.clear();

        // append this new class
        return this.append(Constructor, ...args);
    }

    /**
     *  Method to clear the container.
     *  @return this
     */
    clear() {

        // remove all instances
        this[instances].forEach((instance) => { instance.remove(); });
        
        // drop the references to all instances
        this[instances].length = 0;

        // allow chaining
        return this;
    }

    /**
     *  Cleanup.
     */
    remove() {

        // clear all instances
        this.clear();

        // drop the reference
        this[instances] = null;

        // remove the container
        this[container].remove();

        // drop the reference
        this[container] = null;
    }
};

/**
 *  Proxy class definition that exposes two additional methods: "on" and "off".
 *  These reflect the native `EventTarget.addEventListener` and 
 *  `removeEventListener` methods.
 */
export const EventContainer = (() => new Proxy(Container, {

    /**
     *  Constructor trap.
     *  @param  Object      Target constructor
     *  @param  variadic    Additional arguments.
     */
    construct(Target, args) {

        // construct a new container
        const target = new Target(...args);

        // expose the object as another proxy, in which we can intercept 
        // method calls
        return new Proxy(target, {

            /**
             *  Getter method trap.
             *  @param  Object  Target object.
             *  @param  String  Name of the method of property called.
             *  @return mixed
             */
            get(target, property) {

                // check if we called "on"
                if (property == "on") return (...args) => target[container].addEventListener(...args);

                // check if we called "off"
                if (property == "off") return (...args) => target[container].removeEventListener(...args);

                // return the original call
                if (property in target) return target[property];
            }
        });
    }
}))();
