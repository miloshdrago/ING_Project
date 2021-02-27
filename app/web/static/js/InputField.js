/**
 *  Class for creating a basic form input field. This acts as a base for all
 *  other, more specific form input types.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/InputField.js
 *  @scope  public
 */

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');
const input = Symbol('input');

/**
 *  Function to assign multiple attriutes to an element.
 *  @param  Element Element to assign the attributes to.
 *  @param  Object  Collection of attributes.
 */
const setAttributes = (el, attr = {}) => {

    // iterate over the attributes
    Object.keys(attr).forEach((name) => {

        // assign the attribute to the element
        if (typeof attr[name] != 'undefined') el.setAttribute(name, attr[name]);
    });
};

/**
 *  Export class definition.
 */
export class InputField {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for this class. Supported options are:
     *
     *                      @see    https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement
     *                      +
     *                      "label"         Label of the input field.
     *                      "name"          REQUIRED
     */
    constructor(parent, config = {}) {

        /**
         *  Element for the encapsulating the input.
         *  @var    Element
         */
        this[container] = parent.appendChild(document.createElement('div'));

        /**
         *  Optional label.
         *  @var    Element
         */
        if (config.label) this[container].appendChild(document.createElement('label')).textContent = config.label;

        /**
         *  Element for the input.
         *  @var    Element
         */
        this[input] = this[container].appendChild(document.createElement('input'));

        // set the name
        this[input].setAttribute('name', config.name);

        /**
         *  Applicable attributes for an input element.
         *  @var    Object
         */
        const attributes = Object.assign({}, config);

        // exclude any non-applicable attributes
        delete attributes.label;
        delete attributes.name;

        // assignment of all attributes.
        setAttributes(this[input], attributes);
    }

    /**
     *  Getter method to get the name of the input.
     *  @return String
     */
    get name() {

        // expose the name attribute
        return this[input].getAttribute('name');
    }

    /**
     *  Getter method to get the value of the input.
     *  @return mixed
     */
    get value() {

        // expose the value of the input
        return this[input].value;
    }

    /**
     *  Setter method to set the value of the input.
     *  @param  mixed   Value to set.
     */
    set value(newValue) {

        // set the value of the input
        this[input].value = newValue;
    }

    /**
     *  Cleanup.
     */
    remove() {

        // remove the input field
        this[input].remove();

        // drop the reference
        this[input] = null; 

        // remove the container
        this[container].remove();

        // drop the reference
        this[container] = null;
    }
};
