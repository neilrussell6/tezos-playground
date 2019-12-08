Smart Contracts :: SmartPy
===

> IMPORTANT: ``vendor/SmartPyBasic/SmartPy.sh``
> has been modified in the repository, 
> so be sure to port the changes over if you want to download a newer version.

Commands
---

 - ``make smartpy-compile P=<contract path> C="<call>"`` compile single SmartPy contract (path is relative to src/contracts/)
 - ``make smartpy-test`` run all SmartPy contract tests (but only the last test in each file)

Example Flow
---

1. create a module for your contract eg.
   ```bash
   src/contracts/repeater
   ```
2. create a SmartPy test for your contract eg.
   ```bash
   repeater_contract_sptest.py
   ```
   this will include:
   1. fixtures that build your contract
   2. and tests that interact with it and assert on it's state
3. create a SmartPy file for your contract eg.
   ```bash
   repeater_contract.py
   ```
4. run tests:
   ```bash
   make smartpy-test
   ```

Additional resources
---

 - [website](https://smartpy.io/)
 - [docs](https://smartpy.io/demo/reference.html)
 - [Introducing SmartPyBasic](https://medium.com/@SmartPy_io/introducing-smartpybasic-a-simple-cli-to-build-tezos-smart-contract-in-python-f5bd8772b74a)
