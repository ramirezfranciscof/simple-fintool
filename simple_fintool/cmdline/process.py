"""
Module containing the process commands.
"""

import click


@click.option(
    "--source",
    required=False,
    type=str,
    help="Path to a csv file with the prices of the instruments.",
)
@click.command("process")
def cmd_process(source):
    """Start the processing of the source file."""
    from simple_fintool.engine.core_engine import CoreEngine

    engine_instance = CoreEngine()
    engine_instance.process_file(source)
