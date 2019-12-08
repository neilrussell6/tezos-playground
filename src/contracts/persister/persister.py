"""Persister smart contract"""
import smartpy as sp
# import smartpybasic as spb
# from os.path import dirname, join


class PersisterContract(sp.Contract):
    def __init__(self):
        self.init(storage=0)

    @sp.entryPoint
    def repeat(self, params):
        self.data.storage = params

# # We evaluate a contract with parameters.
# contract = PersisterContract()
#
# target_smlse = join(dirname(__file__), 'persister.smlse')
# spb.compileContract(contract, targetDirectory=dirname(__file__), targetSmlse=target_smlse)
