"""
Module containing the root command of the application.
"""

import click

from .database import cmd_database
from .process import cmd_process


@click.group()
def cmd_root():
    """Root command for the application."""


cmd_root.add_command(cmd_database)
cmd_root.add_command(cmd_process)
