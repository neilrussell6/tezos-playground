"""Tezos smart contract storage util"""
from conseil.core import ConseilClient
import json
from dotenv import load_dotenv

load_dotenv('.env')

conseil = ConseilClient()
Account = conseil.tezos.babylonnet.accounts


def print_query(query):
    result = query.all(output='json')
    print(json.dumps(result, indent=4, sort_keys=True))


def find_account_storage(account_address):
    return Account.query(Account.storage) \
        .filter(Account.account_id == account_address)


def find_and_print_account_storage(account_address):
    query = find_account_storage(account_address)
    print_query(query)
