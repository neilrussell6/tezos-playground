"""Doubler smart contract tests"""
import pytest
from pytezos import ContractInterface

from src.contracts.doubler.doubler import DoublerContract
from src.common.smartpy_utils import compile_smartpy_to_micheline as compile


@pytest.fixture
def doubler(request):
    """Return configured instance of Doubler smart contract"""
    contract_path = compile('doubler', DoublerContract, __file__, request.config.cache)
    instance = ContractInterface.create_from(contract_path)
    instance.maxDiff = None
    return instance


# -----------------------------------------
# tests
# -----------------------------------------

@pytest.mark.parametrize('x,expected', [
    (3, 6),
    (7, 14),
])
def test_doubler_doubles_the_provided_value(x, expected, doubler):
    """Should double the provided value."""
    result = doubler.call(x).result(storage=0)
    assert result.storage == expected
