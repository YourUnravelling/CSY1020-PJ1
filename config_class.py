
# TODO Change file name it sucks

class ConfigClass():

    def __init__(self,
                 schema:dict[str:list] = "", # sql schema dict
                 default_settings:dict = {}, # Overrides for settings that are missing
                 custom_commands:dict[str:dict[str:callable]] = {},
                 pk_defaults:dict[str:str] = {}, # [table name : default primary key]
                 vis_defaults:dict[str:str] = {}, # [table name : default visual key] (only for the default primary key)
                 default_table:str = "" # Default table shown on loadup
                 ):
        self.schema = schema # Public, Dictionary schema of the table # TODO Change to raw sql?
        self.default_settings = default_settings
        self.custom_commands = custom_commands
        self.pk_defaults = pk_defaults