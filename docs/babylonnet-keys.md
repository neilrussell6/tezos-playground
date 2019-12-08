Bablyonnet Keys
===


### Create key pair

```bash
./babylonnet.sh client gen keys "<local account name>"
```

> returns SHA256 digest  ``sha256:\w{64}``

### View key pair

```bash
./babylonnet.sh client show address "<local account name>"
```

> returns HASH digest ``\w{64}``

### List key pairs

```bash
./babylonnet.sh client list known addresses
```
 
> returns HASH ``\w{64}`` and Public Key ``\w{54}``