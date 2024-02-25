"""
Module containing the root command of the application.
"""

import click

from simple_fintool.cmdline.database import cmd_database
from simple_fintool.cmdline.process import cmd_process


@click.group()
def cmd_root():
    """Root command for the application."""


cmd_root.add_command(cmd_database)
cmd_root.add_command(cmd_process)

if __name__ == "__main__":
    cmd_root()
