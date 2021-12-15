"""
OCR-D conformant command line interface
"""
import click
from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor

from .processor import OcrdVandalize

@click.command()
@ocrd_cli_options
def cli(*args, **kwargs):
    """
    Do dumb shit with the input data
    """
    return ocrd_cli_wrap_processor(OcrdVandalize, *args, **kwargs)
