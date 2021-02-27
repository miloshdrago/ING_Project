/**
 *  Class for creating a button field that can be appended to a form.
 *
 *  This class triggers the following events:
 *
 *      @event  "click"     When the user has clicked on an instance of this button.
 *                          @param  "target"    Instance that triggered it.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/ButtonField.js
 *  @scope  public
 */

/**
 *  Dependencies.
 */
import { EventBus } from './EventBus.js';

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');

/**
 *  Export class definition.
 */
export class ButtonField extends EventBus(class {}) {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for the button. Supported options are:
     *
     *                  - type: String
     *                      Type of the button.
     *
     *                  - text: String
     *                      Text content of the button.
     */
    constructor(parent, options = {}) {

        // call the parent class
        super();

        /**
         *  Button element.
         *  @var    Element
         */
        this[container] = parent.appendChild(document.createElement('button'));

        /**
         *  Attribute check and assignment to the button.
         */
        if (options.type) this[container].setAttribute('type', options.type);
        if (options.text) this[container].textContent = options.text;

        /**
         *  Event listener for the click event.
         */
        this[container].addEventListener('click', (e) => {

            // trigger the click event
            this.trigger('click', { target: this });
        });
    }

    /**
     *  Cleanup.
     */
    remove() {

        // remove the container
        this[container].remove();

        // drop the reference
        this[container] = null;

        // call the parent class
        super.remove();
    }
};
