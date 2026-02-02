"""
The class for the configuration file
"""

class ConfigClass():
    """
    Class which is referenced, spesific to the database but not included within it.
    """
    def __init__(
            self,
            default_settings:dict = {}, 
            custom_commands:dict[str,dict[str,callable]] = {},
            table_custom_commands:dict[str, dict[str, callable]] = {}, 
            display_keys:dict[str, str] = {},
            default_table:str = "", 
            default_values:dict[str,tuple] = {}, 
            category_contents:list[tuple[str,list[str]|str, bool]] = [("Tables", "*", True)],
            window_name:str = "SQLite Manager"
            ):
        # All public
        self.default_settings =             default_settings        # Overrides for settings that are missing
        self.custom_commands =              custom_commands         # Commands Present anywhere
        self.table_custom_commands =        table_custom_commands   # Commands only displayed when certain tables are viewed
        self.display_keys =                 display_keys            # Keys that are shown when a table is referenced
        self.default_table =                default_table           # Default table shown on loadup
        self.default_values =               default_values          # Default values in a table? TODO del
        self.category_contents =            category_contents       # Contents and order of categories on the sidebar TODO Move to 
        self.window_name =                  window_name             # Window name