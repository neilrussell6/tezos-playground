## Copyright 2019 Smart Chain Arena LLC. ##

# To run this script, we need to setup a PYTHONPATH to the
# SmartPyBasic directory.

# If the SmartPyBasic directory is ~/SmartPyBasic, then
#   PYTHONPATH=~/SmartPyBasic python3 demo.py
# or
#   ~/SmartPyBasic/SmartPy.sh run demo.py
# should work.

import smartpy as sp
# We need to compile the contract.
# It can be done with the following command.
import smartpybasic as spb


class MyContract(sp.Contract):
    def __init__(self, myParameter1, myParameter2):
        self.init(myParameter1 = myParameter1,
                  myParameter2 = myParameter2)
    @sp.entryPoint
    def myEntryPoint(self, params):
        sp.verify(self.data.myParameter1 <= 123)
        self.data.myParameter1 += params

# We evaluate a contract with parameters.
contract = MyContract(12, 13)

spb.compileContract(contract, targetBaseFilename = "/tmp/myContractDemo")

print("Contract compiled in /tmp/myContractDemoCode.tz")
