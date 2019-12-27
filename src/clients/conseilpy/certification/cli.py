"""ConseilPy Command line interface for Certification Tezos smart contract."""

import locale
import logging

import click
import click_log

from src.clients.conseilpy.certification.utils import verify_and_print_student_certification

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

locale.setlocale(locale.LC_ALL, '')


@click.group()
def cert():
    """Certification Tezos smart contract CLI."""
    pass


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-a', '--address', 'student_address', default=None, help='student address to verify')
@click.option('-c', '--contract', 'contract_address', envvar='CERTIFICATION_CONTRACT_ADDRESS', default=None, help='certification smart contract address')
def verify(student_address, contract_address):
    """Verify certification command.

    Verifies that the provided student address is certified.
    """
    if student_address is None:
        student_address = click.prompt('please enter student address')

    if contract_address is None:
        contract_address = click.prompt("""please enter certification smart contract address, 
or set CERTIFICATION_CONTRACT_ADDRESS env var prior to running this command
""")

    click.echo('certification smart contract address: {}'.format(contract_address))
    click.echo('verifying certification for student at address: {} ...'.format(student_address))

    verify_and_print_student_certification(contract_address, student_address)


cert.add_command(verify)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-a', '--address', 'student_address', default=None, help='certified student address')
@click.option('-n', '--name', 'student_name', default=None, help='certified student name')
@click.option('-c', '--contract', 'contract_address', envvar='CERTIFICATION_CONTRACT_ADDRESS', default=None, help='certification smart contract address')
def certify(student_address, student_name, contract_address):
    """Certify command.

    Certifies the provided student address and name.
    """
    if student_address is None:
        student_address = click.prompt('please enter student address')

    if student_name is None:
        student_name = click.prompt('please enter student name')

    if contract_address is None:
        contract_address = click.prompt("""please enter certification smart contract address, 
or set CERTIFICATION_CONTRACT_ADDRESS env var prior to running this command
""")

    click.echo('certification smart contract address: {}'.format(contract_address))
    click.echo('creating certification for student at address: {} with name: {} ...'.format(student_address, student_name))

    certify_and_print_student_certification(contract_address, student_address, student_name)


cert.add_command(verify)


if __name__ == '__main__':
    cert()
