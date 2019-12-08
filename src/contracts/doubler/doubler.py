"""Doubler smart contract"""
import vendor.SmartPyBasic.smartpy as sp


class DoublerContract(sp.Contract):
    def __init__(self):
        self.init(storage=0)

    @sp.entryPoint
    def double(self, value):
        self.data.storage = value + value
