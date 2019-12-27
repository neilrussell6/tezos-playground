"""Certification smart contract"""
import vendor.SmartPyBasic.smartpy as sp


class Certification(sp.Contract):
    """
        certified : list<string>
        certifier : address
    """
    def __init__(self):
        self.init(
            certified=sp.map(tkey=sp.TAddress, tvalue=sp.TString),
            certifier=sp.address('tz1W4W2yFAHz7iGyQvFys4K7Df9mZL6cSKCp'),
        )

    @sp.entryPoint
    def certify(self, params):
        sp.verify(sp.sender == self.data.certifier)
        sp.verify(self.data.certified.contains(params.address) != True)
        self.data.certified[params.address] = params.name

    @sp.entryPoint
    def revoke(self, params):
        sp.verify(sp.sender == self.data.certifier)
        sp.verify(self.data.certified.contains(params.address) == True)
        del self.data.certified[params.address]
