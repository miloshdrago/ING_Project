/**
 *  Class for building mixins. This is useful if you want to share interfaces
 *  through a horizontal hierarchy across classes.
 *
 *  @example    ```
 *              class Foo extends Mixin.mix(Bar).with(Mixin1, Mixin2) {
 *
 *                  // your code...
 *              }
 *              ```
 *
 *  Inspired by: https://github.com/justinfagnani/mixwith.js.
 *  
 *  @author Tycho Atsma <tycho.atsma@gmail.com>
 *  @file   web/static/js/Mixin.js
 *  @scope  public
 */

/**
 *  Private property accessors.
 *  @var    Symbol
 */
const superclass = Symbol('superclass');

/**
 *  Export class declaration.
 */
export class Mixin {

    /**
     *  Constructor.
     *  @param  class   Super class to apply mixins to.
     */
    constructor(_superclass) {

        // reference to the superclass
        this[superclass] = _superclass;
    }

    /**
     *  Method to mix a class.
     *  @param  class   Super class to apply mixins to.
     *  @return Mixin
     */
    static mix(superclass) {

        // expose a new instance
        return new Mixin(superclass);
    }

    /**
     *  Method to install mixins on the superclass.
     *  @param  variadic    List of mixin classes.
     *  @return class
     */
    with(...mixins) {

        // expose the mixed class
        return mixins.reduce((cls, mixin) => mixin(cls), this[superclass]);
    }
};
