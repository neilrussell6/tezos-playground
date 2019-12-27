"""Certification Verifier (written in ConseilPy)"""
from conseil.core import ConseilClient
from dotenv import load_dotenv
import json

load_dotenv('.env')

conseil = ConseilClient()
Account = conseil.tezos.babylonnet.accounts
Operation = conseil.tezos.babylonnet.operations


def find_account_storage(account_address):
    return Account.query(Account.storage) \
        .filter(Account.account_id == account_address)


def verify_and_print_student_certification(contract_address, student_address):
    query = find_account_storage(contract_address)
    result = query.all(output='csv')
    print(student_address in result)


def certify_and_print_student_certification(contract_address, student_address, student_name):
    pass
    # TODO: is this possible? can't find info on writing to contract via ConseilPy
