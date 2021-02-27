/**
 *  Class for containing a form field. This only acts as a container, not to be
 *  the actual field itself, a text field for example.
 *
 *  This can hold one or more of such fields, enforcing a consistent layout
 *  between forms.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/FormField.js
 *  @scope  public
 */

/**
 *  Dependencies.
 */
import { Container } from './Container.js';

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const widgets = Symbol('widgets');

/**
 *  Export class definition.
 */
export class FormField extends Container {
    
    /**
     *  Constructor.
     *  @param  Element Parent element.
     */
    constructor(parent) {

        // call the parent class
        super(parent, { className: 'formfield' });

        /**
         *  Collection of widgets appended to this field.
         *  @var    Array
         */
        this[widgets] = [];
    }

    /**
     *  Method to expose the value of this field.
     *  @return Object
     */
    get value() {

        // reconstruct the value based on the installed fields
        return Object.fromEntries(this[widgets]
            .map((widget) => [widget.name, widget.value])
            .filter(([name, value]) => name));
    }

    /**
     *  Method override of the .append method.
     *  @see Container.append
     */
    append(Constructor, ...args) {

        // call the parent class
        const instance = super.append(Constructor, ...args);

        // remember this instance so we can access it later
        this[widgets].push(instance);

        // expose the instance again
        return instance;
    }
};
