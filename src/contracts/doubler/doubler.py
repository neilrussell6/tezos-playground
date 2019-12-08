"""Doubler smart contract"""
import vendor.SmartPyBasic.smartpy as sp


class DoublerContract(sp.Contract):
    def __init__(self):
        print("--------- DoublerContract :: init")
        self.init(storage=0)

    @sp.entryPoint
    def double(self, value):
        print("--------- DoublerContract :: double")
        self.data.storage = value + value
