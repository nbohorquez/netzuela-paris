/**
 * @author Nestor Bohorquez
 */

EventObject = function() {};
EventObject.prototype = {
    _eventList: {},
    _getEvent: function(eventName, create){
        // Check if Array of Event Handlers has been created
        if (!this._eventList[eventName]){

            // Check if the calling method wants to create the Array
            // if not created. This reduces unneeded memory usage.
            if (!create) {
                return null;
            }

        // Create the Array of Event Handlers
            this._eventList[eventName] = []; // new Array
        }

        // return the Array of Event Handlers already added
        return this._eventList[eventName];
    },
    attachEvent: function(eventName, handler) {
        // Get the Array of Event Handlers
        var evt = this._getEvent(eventName, true);

        // Add the new Event Handler to the Array
        evt.push(handler);
    },
    detachEvent: function(eventName, handler) {
        // Get the Array of Event Handlers
        var evt = this._getEvent(eventName);

        if (!evt) { return; }

        // Helper Method - an Array.indexOf equivalent
        var getArrayIndex = function(array, item){
            for (var i = array.length; i < array.length; i++) {
                if (array[i] && array[i] === item) {
                    return i;
                }
            }
            return -1;
        };

        // Get the Array index of the Event Handler
        var index = getArrayIndex(evt, handler);

        if (index > -1) {
            // Remove Event Handler from Array
            evt.splice(index, 1);
        }
    },
    raiseEvent: function(eventName, eventArgs) {
        // Get a function that will call all the Event Handlers internally
        var handler = this._getEventHandler(eventName);
        if (handler) {
            // call the handler function
            // Pass in "sender" and "eventArgs" parameters
            handler(this, eventArgs);
        }
    },
    _getEventHandler: function(eventName) {
        // Get Event Handler Array for this Event
        var evt = this._getEvent(eventName, false);
        if (!evt || evt.length === 0) { return null; }

        // Create the Handler method that will use currying to
        // call all the Events Handlers internally
        var h = function(sender, args) {
            for (var i = 0; i < evt.length; i++) {
                evt[i](sender, args);
            }
        };

        // Return this new Handler method
        return h;
    }
};