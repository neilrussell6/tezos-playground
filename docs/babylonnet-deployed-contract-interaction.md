Bablyonnet : Interact with deployed contracts
===

### call:

```bash
./babylonnet.sh client transfer <amount> from <account key> to <contract name> -arg <input>
```

or 

```bash
make babylonnet-call C=<contract name> A=<account key> I=<input>
```
eg.
```bash
make babylonnet-call C=persister A=myFirstKey I=13
```
