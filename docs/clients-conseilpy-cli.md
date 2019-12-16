Clients : ConseilPy : example CLI
===

Examples
---

### setup

```bash
make install
```

### contract storage

Retrieve the current storage state of a contract:
```bash
tezos-playground storage -a <contract address>
```
or
```bash
tezos-playground storage
```
and you will be prompted for the contract address

### cerification verifier

> will use ``CERTIFICATION_CONTRACT_ADDRESS`` in ``.env``, or will prompt you if not set
 
Verify that a student is certified:
```bash
tezos-playground cert verify -a <student address>
```
or
```bash
tezos-playground cert verify
```
and you will be prompted for the student address
