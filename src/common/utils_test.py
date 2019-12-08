"""Common Utils tests"""

import pytest
from pytest_cases import fixture_ref, pytest_fixture_plus, pytest_parametrize_plus

from src.common.utils import add, head


@pytest.fixture
def two_numbers():
    """Return two useful numbers"""
    return 13, 23


@pytest.fixture
def different_two_numbers():
    """Return different two useful numbers"""
    return 10, 3


# -----------------------------------------
# tests
# -----------------------------------------

def test_add():
    """Should sum 3 and 5 and return 8."""
    result = add(3, 5)
    assert result == 8


@pytest.mark.parametrize('a,b,expected', [
    (3, 4, 7),
    (5, 4, 9),
])
def test_add_with_params(a, b, expected):
    """Should add the provided numbers as expected."""
    assert add(a, b) == expected


def test_add_with_fixture(two_numbers):
    """Should return 36 as the result of adding the two useful numbers."""
    (a, b) = two_numbers
    assert add(a, b) == 36


@pytest_fixture_plus
@pytest_parametrize_plus('numbers,expected', [
    (fixture_ref(two_numbers), 36),
    (fixture_ref(different_two_numbers), 13),
])
def test_add_with_params_and_fixture2(numbers, expected):
    """Should return the expected sum of the provided useful number combinations."""
    (a, b) = numbers
    assert add(a, b) == expected


@pytest.mark.parametrize('xs,expected', [
    ([1, 2, 3], 1),
    ([4], 4),
    ([], None),
])
def test_head_returns_the_first_element_of_provided_list_or_none(xs, expected):
    """Should return the first element of provided list or None."""
    assert head(xs) == expected
