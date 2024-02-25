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
@click.option(
    "--pandas", is_flag=True, default=False, help="Use pandas for the calculation."
)
@click.command("process")
def cmd_process(source, pandas):
    """Start the processing of the source file."""
    from simple_fintool.engine.core_engine import CoreEngine
    from simple_fintool.engine_df.core_engine import CoreEngineDF

    if pandas:
        engine_instance = CoreEngineDF()
    else:
        engine_instance = CoreEngine()

    engine_instance.process_file(source)
