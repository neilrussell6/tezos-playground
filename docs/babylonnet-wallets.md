Bablyonnet Wallets
===

Create a wallet (from faucet)
---

https://faucet.tzalpha.net/

download new wallet JSON, will include:

 - mnemonic
 - secret
 - amount
 - pkh (public key hash)
 - password
 - email

> The faucet will give you a key pair, which can be used in all test networks. You can also use the Babylonnet Faucet by Baking Bad to receive some tez.

### checks

confirm default user (tezos)
```bash
docker exec babylonnet_node_1 whoami                              
```

confirm default user's group (nogroup)
```bash
docker exec babylonnet_node_1 id -g -n tezos
```

ensure client is bootstrapped
```bash
./babylonnet.sh client bootstrapped
```
returns:
Digest: sha256:d518a234ae1098ebffe080f9a714c5b0a69fa1e1a5e4d21981d99f9d7347d036

### setup account from wallet

copy wallet json to docker container
```bash
docker cp <wallet file>.json babylonnet_node_1:/home/tezos/
```

assign account to tezos account <--improve this
```bash
docker exec babylonnet_node_1 sudo chown tezos:nogroup /home/tezos/<wallet file>.json
```

### activate account

```bash
./babylonnet.sh client activate account <wallet name> with /home/tezos/<wallet file>.json
```
returns:
Account <wallet name> (<hash>) activated with ꜩ<amount>.

### activate account (error)

NOTE: if this step fails then you will get errors like:
```bash
Empty implicit contract (tz...)
transfer simulation failed
```
when you attempt to transfer: ``./babylonnet.sh client transfer`` (next step)
You can go back to the faucet and download a new wallet, but how to fix this?

### transfer

transfer tez from faucet wallet to local account (created with [``./babylonnet.sh client gen keys "<local account>"``](./babylonnet-keys.md)):
```bash
./babylonnet.sh client transfer 1 from <wallet name> to <local account> --burn-cap 0.5
```

### check balance

check local account balance
```bash
./babylonnet.sh client get balance for <local account>
```

should return something like ``1 ꜩ``
