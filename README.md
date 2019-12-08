Tezos Playground
===

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
 - [Babylonnet](docs/babylonnet.md)
 - [Smart Contracts](docs/smart-contracts.md)
 - [IDE Setup](docs/ide-intellij-python.md)
