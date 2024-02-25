"""
Module containing the database commands.
"""

import json
from pathlib import Path

import click


@click.group("database")
def cmd_database():
    """Commands for database operations."""


@cmd_database.command("setup")
def cmd_database_setup():
    """Set up the database."""
    from simple_fintool.database.session import engine
    from simple_fintool.database.tables import Base

    Base.metadata.create_all(bind=engine)


@click.option(
    "--name",
    required=False,
    type=str,
    help="Name of the instrument.",
)
@click.option(
    "--value",
    required=False,
    type=float,
    help="Value for the multiplier.",
)
@click.option(
    "--source",
    required=False,
    type=str,
    help="Path to a json file with the names as keys and multipliers as values.",
)
@cmd_database.command("update")
def cmd_database_update(name, value, source):
    "Update the instrument price modifier entries database."
    from simple_fintool.database.manager import DatabaseManager

    if source is not None and name is None and value is None:

        file_path = Path(source)
        if not file_path.is_file():
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        with open(file_path) as fileobj:
            new_multipliers = json.load(fileobj)

    elif name is not None and value is not None:

        new_multipliers = {name: value}

    else:
        raise ValueError("Provide either a source path OR name and value.")

    manager = DatabaseManager()
    manager.update_multipliers(new_multipliers)


@cmd_database.command("get")
def cmd_database_get():
    "Show all instrument price modifier entries in the database."
    from simple_fintool.database.manager import DatabaseManager

    manager = DatabaseManager()
    results = manager.get_multipliers()
    print(results)
