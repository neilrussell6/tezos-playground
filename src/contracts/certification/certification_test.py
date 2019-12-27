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
    'tz1Tb8ZBnjiK55rsWqoAnE6eoAYr2iAk5nUE',
])
def test_certify_adds_the_provided_student_to_the_mapping_of_certified_students(certifier_address, certification):
    """Should add the provided student to the mapping of certified students."""
    student1_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    student2_address = 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa'
    result = certification \
        .certify(name='STUDENT 1', address=student1_address) \
        .result(
        storage={
            'certified': [],
            'certifier': certifier_address,
        },
        sender=certifier_address,
    )
    assert len(result.storage['certified']) == 1
    assert student1_address in result.storage['certified']
    assert result.storage['certified'][student1_address] == 'STUDENT 1'

    result = certification \
        .certify(name='STUDENT 2', address=student2_address) \
        .result(
            storage=result.storage,
            sender=certifier_address,
        )
    assert len(result.storage['certified']) == 2
    assert student1_address in result.storage['certified']
    assert result.storage['certified'][student1_address] == 'STUDENT 1'
    assert student2_address in result.storage['certified']
    assert result.storage['certified'][student2_address] == 'STUDENT 2'


def test_certify_does_not_allow_non_admin_to_certify_students(certification):
    """Should not allow non-admin to certify students."""
    certifier_address = 'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9'
    student1_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    non_certifier_address = 'tz1Tb8ZBnjiK55rsWqoAnE6eoAYr2iAk5nUE'
    with pytest.raises(MichelsonRuntimeError, match=r"WrongCondition(.*?)sender(.*?)certifier"):
        certification\
            .certify(name='STUDENT 1', address=student1_address)\
            .result(
                storage={
                    'certified': [],
                    'certifier': certifier_address,
                },
                sender=non_certifier_address,
            )


def test_certify_does_not_allow_duplicate_certifications(certification):
    """Should not allow duplicate certifications."""
    certifier_address = 'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9'
    student1_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    result = certification \
        .certify(name='STUDENT 1', address=student1_address) \
        .result(
            storage={'certified': {}, 'certifier': certifier_address},
            sender=certifier_address,
        )
    assert len(result.storage['certified']) == 1
    assert student1_address in result.storage['certified']
    assert result.storage['certified'][student1_address] == 'STUDENT 1'

    with pytest.raises(MichelsonRuntimeError, match=r"WrongCondition"):
        certification \
            .certify(name='STUDENT 1 AGAIN', address=student1_address) \
            .result(storage=result.storage, sender=certifier_address)


# better testing approach than previous
def test_certify_does_not_allow_duplicate_certifications2(certification):
    """Should not allow duplicate certifications."""
    certifier_address = 'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9'
    student_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    storage = {'certified': {student_address: 'STUDENT 1'}, 'certifier': certifier_address}

    with pytest.raises(MichelsonRuntimeError, match=r"WrongCondition"):
        certification \
            .certify(name='STUDENT 1 AGAIN', address=student_address) \
            .result(storage=storage, sender=certifier_address)


def test_revoke_removes_the_provided_student_from_the_mapping_of_certified_students(certification):
    """Should remove the provided student from the mapping of certified students."""
    certifier_address = 'tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9'
    student1_address = 'tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'
    student2_address = 'tz1Tb8ZBnjiK55rsWqoAnE6eoAYr2iAk5nUE'

    # given ... 2 students already certified
    storage = {'certified': {student2_address: 'STUDENT 2', student1_address: 'STUDENT 1'}, 'certifier': certifier_address}

    # when ... we revoke students 1's certification
    result = certification \
        .revoke(student1_address) \
        .result(storage=storage, sender=certifier_address)

    # then ... should now only have student 1 as certified
    assert len(result.storage['certified']) == 1
    assert student1_address not in result.storage['certified']
    assert student2_address in result.storage['certified']
    assert result.storage['certified'][student2_address] == 'STUDENT 2'


def test_revoke_does_not_allow_non_admin_to_revoke_student_certification(certification):
    """Should not allow non-admin to revoke student certification."""
    # TODO: test
    pass


def test_revoke_not_allow_us_to_attempt_to_revoke_non_certified_student_certification():
    """Should not allow us to attempt to revoke non-certified student certification."""
    # TODO: test
    pass

{certified: {}, certifier: "tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9"}
