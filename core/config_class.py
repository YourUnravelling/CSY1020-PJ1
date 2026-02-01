
# TODO Change file name it sucks

class ConfigClass():

    def __init__(
            self,
            #schema:dict[str,list] = "", # sql schema dict
            default_settings:dict = {}, # Overrides for settings that are missing
            custom_commands:dict[str,dict[str,callable]] = {},
            table_custom_commands:dict[str, dict[str, callable]] = {}, # Commands only displayed when this table is viewed
            #pk_defaults:dict[str,str] = {}, # [table name : default primary key] TODO del
            #vis_defaults:dict[str,str] = {}, # [table name : default visual key] (only for the default primary key) TODO del
            default_table:str = "", # Default table shown on loadup
            default_values:dict[str,tuple] = {}, # Default values in a table? TODO del
            category_contents:list[tuple[str,list[str]|str, bool]] = [("Tables", "*", True)]
            ):
        # All public
        #self.schema = schema
        self.default_settings = default_settings
        self.custom_commands = custom_commands
        self.table_custom_commands = table_custom_commands
        #self.pk_defaults = pk_defaults
        #self.vis_defaults = vis_defaults
        self.default_table = default_table
        self.default_values = default_values
        self.category_contents = category_contents