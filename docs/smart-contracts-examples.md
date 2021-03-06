Smart Contracts :: Examples
===

### Michelson + BabylonNet

Here is an example of a Michelson Smart Contract, with no automated tests:
```bash
contracts/persister/persister.tz
```

To manually "test" it on BabylonNet run:
```bash
make babylonnet-test C=persister S=0 V=5
```
To type check it on BabylonNet run:
```bash
make babylonnet-typecheck C=persister
```

For more info see [Michelson + BabylonNet](smart-contracts-babylonnet.md).

### Michelson + PyTezos

Here is an example of a Michelson Smart Contract:
```bash
src/contracts/concat/concat.tz
```
And a test for it written in PyTest (with the help of PyTezos):
```bash
contracts/concat/concat_contract_test.py
```

To test it run:
```bash
make test
```
Or to test it in watch mode run:
```bash
make test-watch
```

For more info see [Michelson + PyTezos](smart-contracts-pytezos.md).

### SmartPy

Here are examples of a SmartPy Smart Contracts:
```bash
contracts/persiter/persiter.py
```
And here are tests for them, also written in SmartPy:
```bash
contracts/persiter/persiter.py
```

To run these tests:
```bash
make smartpy-test
```
Will match SmartPy tests as files matching the following:
```bash
contracts/**/*_sptest.py
```

For more info see [SmartPy](smart-contracts-smartpy.md)
