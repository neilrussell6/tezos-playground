Smart Contracts :: Michelson + BabylonNet
===

Commands
---

 - ``make babylonnet P=8732`` start BabylonNet on port 8732
 - ``make babylonnet-stop`` stop BabylonNet
 - ``make babylonnet-status`` check BabylonNet status
 - ``make babylonnet-test`` "test" single Smart Contract on BabylonNet
 - ``make babylonnet-typecheck`` type check a single Smart Contract on BabylonNet

Example flow
---

1. start BabylonNet
   ```bash
   ./dependencies/babylonnet/babylonnet.sh start --rpc-port 8732
   ```
   or
   ```bash
   make babylonnet P=8732
   ```
2. create a module for your contract eg.
   ```bash
   src/contracts/duplicator
   ```
3. create a Michelson file for your contract eg.
   ```bash
   duplicator_contract.tz
   ```
4. test your contract on BabylonNet eg.
   ```bash
   ./dependencies/babylonnet/babylonnet.sh client run script container:<path to contract> on storage <storage> and input <input>
   ```
   or
   ```bash
   make babylonnet-test C=<module & contract name> S=<storage> V=<input>
   make babylonnet-test C=duplicator S=0 V=5
   ```
5. type check your contract on BabylonNet eg.
   ```bash
   ./dependencies/babylonnet/babylonnet.sh client typecheck script container:<path to contract> -details
   ```
   or
   ```bash
   make babylonnet-typecheck C=<module & contract name>
   make babylonnet-typecheck C=duplicator
   ```

Additional resources
---

 - [docs](https://github.com/baking-bad/pytezos)
