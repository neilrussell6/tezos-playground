smartpy.io : deployed contract interaction
===

### You can interact with deployed testnet contract on [smartpy.io](https://smartpy.io):
 
 1. go to [Tezos Faucet Importer](https://smartpy.io/demo/faucetImporter.html)
 2. paste in wallet JSON data
 3. generate private key
 4. select ``https://tezos-dev.cryptonomic-infra.tech`` node
 5. follow remaining steps
 6. returning to [Editor](https://smartpy.io/demo/index.html)
 7. under **Michelson** tab on the right click **Deploy Contract**
 8. on deployment page, paste in generated private key 
 9. select ``https://tezos-dev.cryptonomic-infra.tech`` node
 10. click **Deploy Contract**
 11. for [interaction with this deployed contract](smartpyio-contract-interaction.md) you will need the deployed contract address,
     which can be found in the output panel either here:
     ```
     OriginatedContract: KT...
     ```
     or at this path in the JSON:
     ```
     results.contents[0].metadata.operation_result.originated_contracts[0]
     ```
