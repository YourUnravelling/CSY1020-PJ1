"""
The base classes for all panels
"""

from gui.widgets import DFrame


class BasePanel(DFrame):
    """
    The base class of all panels, used for panels which don't control the object of other panels
    """
    current_id:int = 0 # Used to set the id of panels

    def __init__(self, master, core, update_function, debug_name: str | None = None, cnf={}, **kw):
        super().__init__(master, debug_name, cnf, **kw)
        self._core = core # Protected, a pointer to core
        self.__update_function = update_function # Private, function which is called which updates all other panels

        self._object:dict = {}

        # Setting uid to a unique value
        self.uid = BasePanel.current_id
        BasePanel.current_id += 1
    
    def set_object(self, object:dict, force:bool=False):
        """
        Sets the object by updating the panel's attribute with object params and calls the spesific panel's update method
        
        :param object: Object(s) to update
        :type object: dict
        :param force: Forces an update even if the object is the same
        :type force: bool
        """
        keys = object.keys()
        objects_to_update:set = set()
        
        for key in keys:
            # If the key isn't already present in object property, add it to avoid errors
            if not key in self._object.keys():
                self._object[key] = object[key]
                objects_to_update.add(key) # Also add to updated objs because adding the object is updating it
                continue

            # If old object key value matches new object key value
            if self._object[key] != object[key]: 
                self._object[key] = object[key] # Update object value to have the new object value
                objects_to_update.add(key)
        
        if force: # If force is true set everything to updated
            for key in keys:
                objects_to_update.add(key)
            print("[Basepanel] Update being forced,", keys, objects_to_update, self)

        if objects_to_update or force: # Needs an or force here because of table selectors
            print("[Basepanel] Updating the object", self, self._object, object, objects_to_update)
            self._set_object_spesific(objects_to_update)
        else:
            print("[Basepanel] Tried to update object but it was not changed")
    
    def signal_updated_object(self, updated_object:dict, caller_uid):
        """
        Sends a signal that an object was updated, and if that object is contained within the updated one it's refreshed
        caller uid is the id of the object that called the update, and thus is not updated
        """
        cur_obj:dict = self._object
        print("An updated object signal is being broadcast by", self, "of", self._object)

        need_to_refresh:bool = False

        print("Updated object:", updated_object, "Current object:", cur_obj, self)
        # TODO God please generalise this
        if not cur_obj or not updated_object:
            return

        for i in range(1): # To allow break statements
            if updated_object["table"] == cur_obj["table"] and (not "record" in cur_obj) and (not "field" in cur_obj):
                need_to_refresh = True
                break
            
            if updated_object["table"] == cur_obj["table"] and updated_object["record"] == cur_obj["record"] and (not "field" in cur_obj):
                need_to_refresh = True
                break
            
            if updated_object["table"] == cur_obj["table"] and updated_object["record"] == cur_obj["record"] and updated_object["field"] == cur_obj["field"]:
                need_to_refresh = True
                break
        
        # Don't update if caller is pointing to this object, however do if caller is null
        if caller_uid:
            if self.uid == caller_uid:
                need_to_refresh = False

        if need_to_refresh:
            self.set_object(cur_obj, force=True)

    def _set_object_spesific(self, updated_objects:set[str] = set()) -> None:
        """
        To be overwritten by child classes.
        """
        raise NotImplementedError

    def _broadcast_object_update(self, updated_object:dict):
        """
        Broadcasts an object update
        """
        self.__update_function(updated_object, self.uid)

class BindablePanel(BasePanel):
    """
    Panel which can have its selected object bound to one or more methods
    """
    def __init__(self, master, core, update_function, debug_name: str | None = None, cnf={}, **kw):
        super().__init__(master, core, update_function, debug_name, cnf, **kw)
        self.__binds = [] # Private, list of binds to be called when selected object is updated.

    def add_bind(self, bind_callable):
        """
        Adds a callable, called with object as param when this panel updates its selected object
        """
        self.__binds.append(bind_callable)

    def remove_bind(self, bind_to_remove):
        """Removes a bound callable"""
        self.__binds.remove(bind_to_remove)

    def _call_binds(self, object:dict) -> None:
        """
        Calls all bound callables with specified object as params
        """
        for bind in self.__binds:
            print("[Bindablepanel] A bindable is being called by", self, "as object", object)
            bind(object)

# TODO for revamp Function in basepanel which returns true if it needs to be updated, which be default just matches the object but can be overwritten
# Maybe even have exact notes on which record and field(s) have changed?