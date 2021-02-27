/**
 *  Class for constructing a form.
 *
 *  This class triggers the folllowing events:
 *
 *      @event  "submit"    When the user submits the form.
 *                          @param  "target"    Instance that triggered the event.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Form.js
 *  @scope  public
 */

/**
 *  Dependencies.
 */
import { EventContainer } from './Container.js';
import { FormField } from './FormField.js';
import { InputField } from './InputField.js';
import { TextField } from './TextField.js';
import { NumberField } from './NumberField.js';
import { ButtonField } from './ButtonField.js';
import { EventBus } from './EventBus.js';

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const container = Symbol('container');

/**
 *  Export class definition.
 */
export class Form extends EventBus(class {}) {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for the form. Supported options are:
     *
     *                      "fields"    Array   List of fields beloning to the form.
     *                      "className" String  Name of the class of the form.
     */
    constructor(parent, options = {}) {

        // call the parent class
        super();

        /**
         *  Container for managing all fields and inputs.
         *  @var    EventContainer
         */
        this[container] = new EventContainer(parent, {
            element: 'form',
            className: options.className
        });

        /**
         *  Retrigger submit events.
         */
        this[container].on('submit', (e) => {

            // prevent default behavior
            e.preventDefault();

            // trigger the submit event to the outside world
            this.trigger('submit', {
                target: this
            });
        });

        // we need to check if we need to define some fields already
        if (options.fields) options.fields.forEach((field) => {

            // create a button field
            if (field.button) this.button(field);

            // create an input field
            else this.input(field);
        });
    }

    /**
     *  Method to expose the data of the form.
     *  @return Object
     */
    data() {

        // form data container
        const data = { };

        // iterate over the installed fields and assign them to the data
        this[container].installed
            .map((instance) => instance.value)
            .filter((value) => Object.keys(value).length)
            .forEach((value) => Object.assign(data, value));

        // expose the values of all fields
        return data;
    }

    /**
     *  Method to add a form field to the form.
     *  @return FormField
     */
    field() {

        // expose the newly constructed form field
        return this[container].append(FormField);
    }

    /**
     *  Method to add an input field.
     *  @param  Object  Configuration for the field. Should at least contain
     *                  a "name" and "type" property. See InputField for more info.
     *  @return InputField
     */
    input(config = {}) {

        // add a new input field
        return this.field().append(InputField, config);
    }

    /**
     *  Method to add a text input field.
     *  @param  Object  Configuration for the field. Should at least contain a
     *                  "name" property. See TextField for more info.
     *  @return TextField
     */
    text(config = {}) {

        // add a new text field
        return this.field().append(TextField, config);
    }

    /**
     *  Method to add a number input field.
     *  @param  Object  Configuration for the field. Should at least contain a
     *                  "name" property. See numberField for more info.
     *  @return numberField
     */
    number(config = {}) {
        
        // add a new number field
        return this.field().append(NumberField, config);
    }

    /**
     *  Method to add a button field.
     *  @param  Object  Configuration for the button field.
     *  @return ButtonField
     */
    button(config = {}) {

        // add a new button field
        return this.field().append(ButtonField, config);
    }

    /**
     *  Cleanup.
     */
    remove() {

        // remove the container
        this[container].remove();

        // drop the reference
        this[container] = null;
    }
};
