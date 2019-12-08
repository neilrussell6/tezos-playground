"""Concat smart contract tests"""

from os.path import dirname, join

import pytest
from pytezos import ContractInterface


@pytest.fixture
def concat():
    """Return configured instance of Concat smart contract"""
    instance = ContractInterface.create_from(join(dirname(__file__), 'concat.tz'))
    instance.maxDiff = None
    return instance


# -----------------------------------------
# tests
# -----------------------------------------

@pytest.mark.parametrize('storage,x,expected', [
    ('foo', 'bar', 'foobar'),
    ('hello', 'world', 'helloworld'),
])
def test_contact_concatenates_the_provided_value_onto_current_storage_value(storage, x, expected, concat):
    """Should concatenate the provided value onto current storage value."""
    result = concat.call(x).result(storage=storage)
    assert result.storage == expected
