Bablyonnet
===

 - [Contracts](babylonnet-contracts.md)
 - [Deployment](babylonnet-deployment.md)
 - [Deployed Contract Interaction](babylonnet-deployed-contract-interaction.md)
 - [Keys](babylonnet-keys.md)
 - [Wallets](babylonnet-wallets.md)

Setup
---

### download and start Babylonnet

```bash
http https://gitlab.com/tezos/tezos/raw/babylonnet/scripts/alphanet.sh -d -o babylonnet.sh
chmod +x babylonnet.sh
```

Usage
---

> ./babylonnet.sh behaves as a tezos-client. So use this to interact with the Docker node container.

### Help

```bash
docker logs babylonnet_node_1 --follow
```

### Start Babylonnet

```bash
./babylonnet.sh man
./babylonnet.sh client man
```

### Show Babylonnet's running containers

```bash
docker ps --format '{{printf "%-40s" .Names}} {{.Status}}'
```

### Monitor Balylonnet logs

```bash
docker logs babylonnet_node_1 --follow
```

### Keys / Wallets etc

 - [keys](./babylonnet-keys.md)
 - [wallets](./babylonnet-wallets.md)

### Contracts

 - [contracts](./babylonnet-contracts.md)

### Start on a port

```bash
./babylonnet.sh start --rpc-port 8732
```
this allows HTTP queries to local blockchain eg.
```
curl -s localhost:8732/chains/main/blocks/head/context/contracts/MYFIRSTKEY_ADDRESS/balance
```

Update
---

### Update Babylonnet

stop 
```bash
./babylonnet.sh stop
./babylonnet.sh update_script
chmod +x babylonnet.sh
```

Suggested Bash aliases
---

```bash
alias dps="docker ps --format '{{printf \"%-40s\" .Names}} {{.Status}}'"
```
