"""ConseilPy Command line interface for Tezos playrgound."""

import locale
import logging

import click
import click_log

from src.clients.conseilpy.storage.cli import storage as storage_cli
from src.clients.conseilpy.certification.cli import cert as certification_cli

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

locale.setlocale(locale.LC_ALL, '')


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Tezos Playground CLI."""
    pass


cli.add_command(storage_cli)
cli.add_command(certification_cli)


if __name__ == '__main__':
    cli()
