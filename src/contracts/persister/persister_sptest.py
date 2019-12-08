"""Persister smart contract SmartPy tests"""
import smartpy as sp
from src.contracts.persister.persister import PersisterContract


@addTest(name="test_1")  # noqa: F821
def test1():
    """Should persist the provided value as contract storage"""
    contract = PersisterContract()
    scenario = sp.testScenario()

    scenario.register(contract, show=True)
    scenario += contract.repeat(3)
    scenario += contract.repeat(5)
    scenario += contract.repeat(7)

    scenario.verify(contract.data.storage == 7)
