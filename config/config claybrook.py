"""
All variables spesific to the database, including the schema, and functions
"""
# TODO Decide if this should be a class that is instanciated to defaultise var names, would make functions more complex?
# Or just a regular file with spesific var names

from core.config_class import ConfigClass

table_sqls_old = {
    "tables": [
        ["book", "isbn TEXT PRIMARY KEY, author INTEGER, title TEXT, date_published DATE, genre TEXT, price NUMBER"],
        ["author", "id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, surname TEXT, nationality TEXT"],
        ["customer", "id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, surname TEXT, phone TEXT, email TEXT"],
        ["invoice", "id INTEGER PRIMARY KEY AUTOINCREMENT, customer INTEGER, book INTEGER"]
    ]
}
table_sqls = {}


def generate_invoice(record):...

# Old config class for bs
bsc = ConfigClass(
    schema=table_sqls,
    default_settings={},
    custom_commands= {
        "invoice": [generate_invoice]
    },
    default_table="book",
    pk_defaults = {
        "book": "isbn",
        "author": "id",
        "invoice": "id",
        "customer": "id",
    },
    default_values = {
        "book": ("", "", "", "", "", ""),
        "author": ("", "", "", ""),
        "customer": ("", "", "", "", ""),
        "customer": ("", "", "")
    }
)


c = ConfigClass(
    schema=table_sqls,
    default_settings={},
    custom_commands= {
        "invoice": [generate_invoice]
    },
    default_table="author",
    category_contents = [
        ("Animal data", ["Animal", "AnimalMeasurement", "AnimalMedicalNote"]),
        ("Species data", ["Species", "BirdInfo","FishInfo", "FishColor", "MammalInfo", "PlumageColor", "ReptileAmphibianInfo"]),
        ("Sponsor data", []),
        ("Membership data", []),
        ("Visitor data", []),
    ] # type: ignore
    #table_categories = ["Animal data", "Species data", "Sponsor data", "Membership data", "Visitor data"]

    #pk_defaults = {
    #    "book": "isbn",
    #    "author": "id",
    #    "invoice": "id",
    #    "customer": "id",
    #},
    #default_values = {
    #    "book": ("", "", "", "", "", ""),
    #    "author": ("", "", "", ""),
    #    "customer": ("", "", "", "", ""),
    #    "customer": ("", "", "")
    #}
)
