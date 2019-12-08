Bablyonnet Contracts
===

Test contract
---

test
```bash
./babylonnet.sh client run script container:<name>.tz on storage <initial storage> and input <input>
```

inspect stack changes
```bash
./babylonnet.sh client typecheck script container:<contract name>.tz -details
```

Deploy contract
---

```bash
./babylonnet.sh client originate contract <contract name> transferring 0.1 from <local account> running container:<contract name>.tz --init 0 --burn-cap 0.295
```

List contracts
---

```bash
./babylonnet.sh client list known contracts
```

Contract Transaction
---

```bash
./babylonnet.sh client transfer 0 from <local account> to <contract name> --arg "1"
```
returns operation hash eg.
```bash
Operation hash is 'oohUbi7VBDM16HUurdms2qcyMxQqm9ELe92bhJYmWmL1C8tQgge'
```

find transaction by returned hash here:
```
https://better-call.dev/babylon/<operation hash>
```

or see all transactions for contract here:
```
https://better-call.dev/babylon/<contract address>/operations
```

JSON RPC
===

[docs](https://tezos.gitlab.io/api/rpc.html)

List JSON RPC commands
---

```bash
./babylonnet.sh client rpc list
```

view local account:
```bash
./babylonnet.sh client rpc get /chains/main/blocks/head/context/
contracts/<account address>
```
view local account balance:
```bash
./babylonnet.sh client rpc get /chains/main/blocks/head/context/
contracts/<account address>/balance
```
view local account balance (JSON):
```bash
./babylonnet.sh client -l rpc get /chains/main/blocks/head/context/
contracts/<account address>/balance
```
> use ``-l`` flag with any command to see the HTTP requests and the JSON responses the client does