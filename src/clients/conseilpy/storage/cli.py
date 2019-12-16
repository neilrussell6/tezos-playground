"""ConseilPy Command line interface for Tezos smart contract storage."""

import locale
import logging

import click
import click_log

from src.clients.conseilpy.storage.utils import find_and_print_account_storage

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

locale.setlocale(locale.LC_ALL, '')


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-a', '--address', 'address', default=None, help='contract address to retrieve storage from')
def storage(address):
    """Storage command."""
    if address is None:
        address = click.prompt('please enter contract address')

    click.echo('retrieving storage for contract at address: {} ...'.format(address))

    find_and_print_account_storage(address)
