"""
All variables spesific to the database, including the schema, and functions
"""
# TODO Decide if this should be a class that is instanciated to defaultise var names, would make functions more complex?
# Or just a regular file with spesific var names

from core.config_class import ConfigClass


def generate_invoice(record):...

# Old config class for bs
c = ConfigClass(
    default_settings={},
    custom_commands= {
        "invoice": [generate_invoice]
    },
    default_table="book",
    category_contents = [
        ("Tables", ["book", "author", "customer", "customer"], True),
    ]
)