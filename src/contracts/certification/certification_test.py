"""Certification smart contract tests"""
import pytest
from pytezos import ContractInterface, MichelsonRuntimeError

from src.contracts.certification.certification import Certification
from src.common.smartpy_utils import compile_smartpy_to_micheline as compile


@pytest.fixture
def certification(request):
    """Return configured instance of Certification smart contract"""
    contract_path = compile('certification', Certification, __file__, request.config.cache)
    instance = ContractInterface.create_from(contract_path)
    instance.maxDiff = None
    return instance


# -----------------------------------------
# tests
# -----------------------------------------

@pytest.mark.parametrize('certifier_address', [
    'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9',
    'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp',
])
def test_certify_pushes_the_provided_student_to_the_list_of_certified_students(certifier_address, certification):
    """Should push the provided student to the list of certified students."""
    result = certification.call('STUDENT 1').result(
        storage={
            'certified': [],
            'certifier': certifier_address,
        },
        sender=certifier_address,
    )
    assert len(result.storage['certified']) == 1
    assert result.storage['certified'][0] == 'STUDENT 1'

    result = certification.call('STUDENT 2').result(
        storage=result.storage,
        sender=certifier_address,
    )
    assert len(result.storage['certified']) == 2
    assert result.storage['certified'][0] == 'STUDENT 2'
    assert result.storage['certified'][1] == 'STUDENT 1'


def test_certify_does_not_allow_non_admin_to_certify_students(certification):
    """Should not allow non-admin to certify students."""
    certifier_address = 'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9'
    non_certifier_address = 'tz1Tb8ZBnjiK55rsWqoAnE6eoAYr2iAk5nUE'
    with pytest.raises(MichelsonRuntimeError, match=r"WrongCondition(.*?)sender(.*?)certifier"):
        certification\
            .call('STUDENT 1')\
            .result(
                storage={
                    'certified': [],
                    'certifier': certifier_address,
                },
                sender=non_certifier_address,
            )
