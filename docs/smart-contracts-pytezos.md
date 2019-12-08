Smart Contracts :: Michelson + PyTezos
===

Setup
---

install
```bash
brew tap cuber/homebrew-libsecp256k1
$ brew install libsodium libsecp256k1 gmp
```

Commands
---

 - ``make test`` run all PyTest unit tests
 - ``make test-watch`` run all PyTest uuit tests (in watch mode)

Example Flow
---

1. create a module for your contract eg.
   ```bash
   src/contracts/concat
   ```
2. create a PyTest test for your contract eg.
   ```bash
   concat_contract_test.py
   ```
   this will include:
   1. fixtures that build your contract
   2. and tests that interact with it and assert on it's state
3. create a Michelson file for your contract eg.
   ```bash
   concat_contract.tz
   ```
4. run tests:
   ```bash
   make test
   ```
   or
   ```bash
   make test-watch
   ```

Additional resources
---

 - [docs](https://github.com/baking-bad/pytezos)
