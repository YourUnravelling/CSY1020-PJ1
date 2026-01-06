from gui.widgets import DFrame


class BasePanel(DFrame):
    """
    Docstring for BasePanel
    """
    def __init__(self, master, core, debug_name: str | None = None, cnf={}, **kw):
        super().__init__(master, debug_name, cnf, **kw)
        self._core = core # Protected, a pointer to core

        self._object:dict = {}
    
    def set_object(self, object:dict, force:bool=False):
        """
        Sets the object by updating the panel's attribute with object params and calls the spesific panel's update method
        
        :param object: Object(s) to update
        :type object: dict
        :param force: Forces an update even if the object is the same
        :type force: bool
        """
        keys = object.keys()

        old_object = dict(self._object) # Use constructor to create a copy
        for key in keys:
            self._object[key] = object[key]

        
        if (old_object != self._object) or force:
            self._set_object_spesific()
        else:
            print("The object was not changed")


    def _set_object_spesific(self) -> None:
        raise NotImplementedError

class BindablePanel(BasePanel):
    """
    Panel which can have its selected object bound to one or more methods
    """
    def __init__(self, master, core, debug_name: str | None = None, cnf={}, **kw):
        super().__init__(master, core, debug_name, cnf, **kw)
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
            print("Calling a bindable")
            bind(object)