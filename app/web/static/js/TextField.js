/**
 *  Class for creating a basic text form input field.
 *
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/TextField.js
 *  @scope  public
 */

/**
 *  Dependencies
 */
import { InputField } from './InputField.js';

/**
 *  Export class definition.
 */
export class TextField extends InputField {

    /**
     *  Constructor.
     *  @param  Element Parent element.
     *  @param  Object  Configuration for this class. Supported options are:
     *
     *                      @see    https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement
     *                      +
     *                      "label"         Label of the input field.
     */
    constructor(parent, config = {}) {

        // call the parent constructor
        super(parent, Object.assign({}, config, {
            type: "text"
        }));
    }
};
