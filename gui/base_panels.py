from gui.widgets import DFrame


class BasePanel(DFrame):
    """
    Docstring for BasePanel
    """
    def __init__(self, master=None, debug_name: str | None = None, cnf=..., **kw):
        super().__init__(master, debug_name, cnf, **kw)