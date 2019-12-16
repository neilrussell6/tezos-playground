Tezos Playground
===

Watch an example of Tezos smart contract TDD, using SmartPy and PyTezos:
[![Watch the video](https://i9.ytimg.com/vi/fvd1HhkGfHY/mq2.jpg?sqp=CN3xs-8F&rs=AOn4CLBPvM-4KrzzyRDeW7TP9sQXQrgonQ)](https://youtu.be/fvd1HhkGfHY)

Setup
---

1. Create local Python virtual env
   ```bash
   make create-venv
   ```

2. The start local Python virtual env
   ```bash
   . venv/bin/activate
   ```

3. Initialize project
   ```bash
   make create-venv
   ```
   this installs all dependencies and creates local env files.

Dependencies
---

 1. Add new Python dependencies to ``requirements.in``
 2. Then run ``make pip-compile`` to generate a new ``requirements.txt``
 3. Then run ``make pip-install`` to install new dependcies from ``requirements.txt``

Additional Docs
---

 - [Notebooks (Jupyter Lab)](docs/jupyter.md)
 - [Testing](docs/testing.md)
 - [Linting](docs/linting.md)
 - [smartpy.io](docs/smartpyio.md)
 - [Babylonnet](docs/babylonnet.md)
 - [Smart Contracts](docs/smart-contracts.md)
 - [Clients](docs/clients.md)
 - [IDE Setup](docs/ide-intellij-python.md)


Certification
---

### Smart Contract

to deploy the smart contract run:
```
make babylonnet-deploy C=certification A=<wallet name> S='(Pair {} "<certifier address>")' B=1.0
```

to call the deployed smart contract run:
```
make babylonnet-call C=certification A=<wallet name> I='(Pair "<student address>" "<student name>")'
```

to view the current storage state of the deployed smart contract run:
```
make babylonnet-contracts C=certification
```
