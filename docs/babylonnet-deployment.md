Bablyonnet : Deployment
===

### deploy contract:

```bash
./babylonnet.sh client originate contract <contract name> transferring 0.1 from <account key> running container:<contract name>.tz --init 0 --burn-cap 0.295
```

or 

```bash
make babylonnet-deploy C=<contract name> A=<account key> S=<intial storage value>
```
eg.
```bash
make babylonnet-deploy C=persister A=myFirstKey S=0
```

### list deployed contracts:

```bash
./babylonnet.sh client list known contracts
```

or 

```bash
make babylonnet-contracts
```

if you get an error like:
```
Counter 87486 already used for contract ...
```
it means that transaction 87486 is probably still in progress, 
eg. if you try to increment it manually you will get:
```
Counter 87487 not yet reached for contract ...
```

this may be because your local node is not synced,
check this by running:
```bash
make babylonnet-compare-sync
```
and comparing the timestamps.
If you recheck and these are the same, try restarting your local node:
```bash
make babylonnet-restart
```
