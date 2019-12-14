# -----------------------------------------------------------
# vars
# -----------------------------------------------------------

SHELL := /bin/bash
REQUIREMENTS_FILE := requirements
STR_TO_LOWERDASH := sed -e 's/\([A-Z]\)/-\L\1/g' -e 's/^-//' -e 's/\s-/-/g'
SOURCE_DIR := src
COMMA := ,

# SmartPy
SMARTPY_FILE := ./vendor/SmartPyBasic/SmartPy.sh
SMARTPY_TEST_SOURCE := src/contracts/**/*_sptest.py
SMARTPY_TEST_OUTPUT_DIR := build/smartpy

# BabylonNet
BABYLONNET_FILE := ./vendor/babylonnet/babylonnet.sh
BABYLONNET_DEFAULT_PORT := 8732

# envs
ENV := local
ENVS := local test
ENV_FILENAME := .env
ENV_TARGET_FILENAME := .env.$(ENV)
ENV_TPL_FILENAME := .env.$(ENV).tpl
ENV_TARGET_DIFF := if [[ -f $(ENV_TARGET_FILENAME) ]]; then sh ./scripts/get-files-key-diff.sh $(ENV_TPL_FILENAME) $(ENV_TARGET_FILENAME); fi

# TODO: do these in a loop
ENV_LOCAL_TPL_DIFF := if [[ -f .env.local.tpl && -f .env.local ]]; then sh ./scripts/get-files-key-diff.sh .env.local .env.local.tpl; fi
ENV_TEST_TPL_DIFF := if [[ -f .env.test.tpl && -f .env.test ]]; then sh ./scripts/get-files-key-diff.sh .env.test .env.test.tpl; fi

# -----------------------------------------------------------
# includes
# -----------------------------------------------------------

# include env file and make print library
-include .env.$(ENV)

# scripts
print_utils := ./scripts/print-utils.sh

# -----------------------------------------------------------
# functions
# -----------------------------------------------------------

# -----------------------------
# print
# -----------------------------

define print
	@$(eval COLOR=$(or $(3),$(MAKE_THEME)))
	@$(eval MOD=$(or $(4),NORMAL))
	@echo $$(sh $(print_utils) $(1) $(2) $(COLOR) $(MOD))
endef

define printList
	@$(eval COLOR=$(or $(2),$(MAKE_THEME)))
	@$(eval MOD=$(or $(3),NORMAL))
	@sh $(print_utils) printList $(1) ";" $(COLOR) $(MOD)
endef

define printDefListItem
	@$(eval COLOR1=$(or $(3),$(MAKE_THEME)))
	@$(eval COLOR2=$(or $(4),$(3),LIGHTER_GREY))
	@$(eval PAD=$(or $(5),$(MAKE_PADDING)))
	@sh $(print_utils) printDefListItem $(1) $(2) $(COLOR1) $(COLOR2) $(PAD)
endef

#------------------------------
# files
#------------------------------

define create-envs
	@cp ".env.$(ENV).tpl" ".env"; \
	for env in $(1); do \
		cp ".env.$${env}.tpl" ".env.$${env}"; \
	done
endef

# -----------------------------------------------------------
# help
# -----------------------------------------------------------

.PHONY: help
help:
	@$(call print,h1,"AVAILABLE OPTIONS")
	@$(call printDefListItem," - init","Copy local files and initial requirements")
	@echo ""
	@$(call print,h3,"ENV")
	@$(call printDefListItem," - init-envs","Recreate all local env files from templates")
	@echo ""
	@$(call print,h3,"DEPENDENCIES")
	@$(call printDefListItem," - pip-compile","Compile Python requirements")
	@$(call printDefListItem," - pip-install","Install Python requirements")
	@echo ""
	@$(call print,h3,"PYTHON ENVIRONMENT")
	@$(call printDefListItem," - create-venv","Create local Python virtual environment.")
	@$(call printDefListItem," - venv","Start local Python virtual environment.")
	@echo ""
	@$(call print,h3,"JUPYTER")
	@$(call printDefListItem," - jupyter","Start Jupyter Lab.")
	@echo ""
	@$(call print,h3,"LINTING")
	@$(call printDefListItem," - lint","Run Python linter.")
	@echo ""
	@$(call print,h3,"PYTEST")
	@$(call printDefListItem," - test","Run all PyTest unit tests.")
	@$(call printDefListItem," - test-watch","Run all PyTest unit tests in watch mode.")
	@echo ""
	@$(call print,h3,"SMARTPY")
	@$(call printDefListItem," - smartpy-test","Run SmartPy tests.")
	@$(call printDefListItem," - smartpy-compile","Compile SmartPy contract (P=<contract path (from src/contracts/)> C=\"<call>\").")
	@echo ""
	@$(call print,h3,"BABYLONNET")
	@$(call printDefListItem," - babylonnet-h","Show BabylonNet help.")
	@$(call printDefListItem," - babylonnet","Start BabylonNet locally.")
	@$(call printDefListItem," - babylonnet-restart","Restart BabylonNet locally.")
	@$(call printDefListItem," - babylonnet-status","Check local BabylonNet status.")
	@$(call printDefListItem," - babylonnet-stop","Stop local BabylonNet.")
	@$(call printDefListItem," - babylonnet-test","Manually test contract interaction on BabylonNet locally (C=<contact name>$(COMMA) S=<storage value>$(COMMA) V=<input value>).")
	@$(call printDefListItem," - babylonnet-typecheck","Type check a contract on BabylonNet locally (C=$(COMMA)<contact name>).")
	@$(call printDefListItem," - babylonnet-addresses","list known addresses on BabylonNet")
	@$(call printDefListItem," - babylonnet-contracts","listing known contracts on BabylonNet")
	@$(call printDefListItem," - babylonnet-deploy","deploy contract to BabylonNet (C=<contact name>)")
	@$(call printDefListItem," - babylonnet-call","call deployed BabylonNet contract using account (C=<contact name>$(COMMA) A=<account key>$(COMMA) I=<input> D?=<dry-run>)")
	@$(call printDefListItem," - babylonnet-compare-sync","compare BabylonNet last sync timestamp with current timestamp")
	@echo ""

# ------------------------------------------------------------
# initialize
# ------------------------------------------------------------

.PHONY: init
init: init-h init-envs init-python post-build
	@$(call print,h3,"... success")

.PHONY: init-h
init-h:
	@$(call print,h3,"initializing ...")

.PHONY: init-envs
init-envs:
	@$(call print,h3,"creating env files from templates ...")
	@cp pytest.ini.tpl pytest.ini
	@$(call create-envs,$(ENVS))

.PHONY: init-python-h
init-python-h:
	@$(call print,h3,"installing Python dependencies ...")

.PHONY: init-python
init-python: init-python-h init-pip pip-compile pip-install

.PHONY: init-pip
init-pip: venv-check
	@$(call print,h3,"installing pip ...")
	@pip install --upgrade pip
	@$(call print,h3,"installing pip-tools ...")
	@pip install pip-tools

.PHONY: post-build
post-build:
	@$(call print,h3,"running postBuild ...")
	@sh postBuild

# -----------------------------
# create-env
# -----------------------------

# TODO: make this more concise
.PHONY: _validate-tpl-envs
_validate-tpl-envs:
ifneq ($(shell $(ENV_LOCAL_TPL_DIFF)),)
	@$(call print,h2,"YOU HAVE ADDED ENVS TO .env.local PLEASE UPDATE .env.local.tpl WITH",LIGHTRED)
	@$(call printList,"$$(echo $$($(ENV_LOCAL_TPL_DIFF)) | tr ' ' ';')",GOLD)
endif
ifneq ($(shell $(ENV_DEV_TPL_DIFF)),)
	@$(call print,h2,"YOU HAVE ADDED ENVS TO .env.dev PLEASE UPDATE .env.dev.tpl WITH",LIGHTRED)
	@$(call printList,"$$(echo $$($(ENV_DEV_TPL_DIFF)) | tr ' ' ';')",GOLD)
endif
ifneq ($(shell $(ENV_PREPROD_TPL_DIFF)),)
	@$(call print,h2,"YOU HAVE ADDED ENVS TO .env.preprod PLEASE UPDATE .env.preprod.tpl WITH",LIGHTRED)
	@$(call printList,"$$(echo $$($(ENV_PREPROD_TPL_DIFF)) | tr ' ' ';')",GOLD)
endif
ifneq ($(shell $(ENV_TEST_TPL_DIFF)),)
	@$(call print,h2,"YOU HAVE ADDED ENVS TO .env.test PLEASE UPDATE .env.test.tpl WITH",LIGHTRED)
	@$(call printList,"$$(echo $$($(ENV_TEST_TPL_DIFF)) | tr ' ' ';')",GOLD)
endif
ifneq ($(shell $(ENV_LOCAL_TPL_DIFF)),)
	@exit 2
endif
ifneq ($(shell $(ENV_DEV_TPL_DIFF)),)
	@exit 2
endif
ifneq ($(shell $(ENV_PREPROD_TPL_DIFF)),)
	@exit 2
endif
ifneq ($(shell $(ENV_TEST_TPL_DIFF)),)
	@exit 2
endif

.PHONY: _validate-target-env
_validate-target-env:
ifneq ($(shell $(ENV_TARGET_DIFF)),)
	@$(call print,h2,"YOU ARE MISSING ENVS PLEASE UPDATE $(ENV_TARGET_FILENAME) WITH",LIGHTRED)
	@$(call printList,"$$(echo $$($(ENV_TARGET_DIFF)) | tr ' ' ';')",GOLD)
	@exit 2
endif

.PHONY: _create-env-from-target-env
_create-env-from-target-env:
	@rm -f $(ENV_FILENAME)
	@echo -e "# ----------------------------------------\n# $(ENV)\n# ----------------------------------------\n" >> $(ENV_FILENAME)
	@cat $(ENV_TARGET_FILENAME) >> $(ENV_FILENAME)

.PHONY: _check-target-env
_check-target-env:
ifeq (,$(wildcard $(ENV_TARGET_FILENAME)))
	@$(call print,h2,"YOU ARE MISSING $(ENV_TARGET_FILENAME) PLEASE RUN \`\`npm run init\`\` OR CREATE MANUALLY")
	@exit 2
endif

.PHONY: _create-env-h
_create-env-h:
	@$(call print,h3,"creating $(ENV_FILENAME) for target environment: $(ENV) ...")

.PHONY: create-env
create-env: _create-env-h _check-target-env _validate-target-env _create-env-from-target-env _create-env-yml-from-target-env

#------------------------------
# dependency
#------------------------------

.PHONY: pip-compile
pip-compile:
# if called directly
ifeq ($(MAKECMDGOALS),pipcompile)
	@$(call print,h3,"compiling requirements ...")
	@pip-compile $(REQUIREMENTS_FILE).in
	@$(call print,h3,"... success")
# if called as dependency
else
	@$(call print_h2,"compiling requirements")
	@pip-compile $(REQUIREMENTS_FILE).in
endif

.PHONY: pip-install
pip-install:
# if was not called called directly (called as dependency)
ifneq ($(MAKECMDGOALS),pipinstall)
	@$(call print_h2,"installing requirements ...")
	@pip install -r $(REQUIREMENTS_FILE).txt
# requirements txt does not exists, so prompt user to run compile
else ifeq (,$(wildcard $(REQUIREMENTS_FILE).txt))
	$(error Requirements are not compiled run make pipcompile first)
# requirements txt exists, so install
else
	@$(call print,h3,"installing requirements ...")
	@pip install -r $(REQUIREMENTS_FILE).txt
	@$(call print,h3,"... success")
endif

#------------------------------
# venv
#------------------------------

.PHONY: create-venv
create-venv:
	@$(call print,h3,"creating local Python virtual environment ...")
	@python3 -m venv ./venv
	@$(call print,h3,"... complete")

.PHONY: venv
venv:
	@$(call print,h3,"starting local Python virtual environment ...")
	@$(eval,"source venv/bin/activate")

.PHONY: venv-check
venv-check:
ifeq ($(shell echo $$VIRTUAL_ENV),)
	@$(call print,error,"please activate local Python virtual environment first (eg. source venv/bin/activate) read README.md")
	exit 2
endif

#------------------------------
# jupyter
#------------------------------

.PHONY: jupyter
jupyter:
	@$(call print,h3,"starting Jupyter Lab ...")
	@JUPYTER_PATH=./ jupyter lab || true

#------------------------------
# linting
#------------------------------

.PHONY: lint
lint: venv-check
	@$(call print,h3,"linting code ...")
	@flake8 $(SOURCE_DIR)
	@$(call print,h3,"... complete")

.PHONY: lint-fix
lint-fix: venv-check
	@$(call print,h3,"fixing lint issues ...")
	@isort -rc $(SOURCE_DIR)
	@$(call print,h3,"... complete")

#------------------------------
# test
#------------------------------

.PHONY: test
test: venv-check
	@$(call print,h3,"running all tests ...")
	@py.test -v
	@$(call print,h3,"... complete")

.PHONY: test-watch
test-watch: venv-check
	@$(call print,h3,"running all tests (in watch mode) ...")
	@ptw

#------------------------------
# smartpy
#------------------------------

.PHONY: smartpy-test
smartpy-test:
	@$(call print,h3,"running SmartPy tests ...")
	@$(SMARTPY_FILE) test $(SMARTPY_TEST_SOURCE) $(SMARTPY_TEST_OUTPUT_DIR)
	@$(call print,h3,"... complete")

.PHONY: smartpy-compile
smartpy-compile: P:=
smartpy-compile: C:=
smartpy-compile: V:=
smartpy-compile:
	@$(call print,h3,"running SmartPy tests locally ...")
	# TODO: make this generic
	@$(SMARTPY_FILE) compile src/contracts/$(P) "$(C)" $(SMARTPY_TEST_OUTPUT_DIR)/$(P)
	@$(call print,h3,"... complete")

#------------------------------
# babylonnet
#------------------------------

.PHONY: babylonnet-h
babylonnet-h:
	@$(call print,h3,"BabylonNet help ...")
	@$(BABYLONNET_FILE) client man

.PHONY: babylonnet
babylonnet: P?=$(BABYLONNET_DEFAULT_PORT)
babylonnet:
	@$(call print,h3,"starting BabylonNet on port $(P) ...")
	@$(BABYLONNET_FILE) start --rpc-port $(P)
	@$(call print,h3,"BabylonNet running on port $(P) ...")

.PHONY: babylonnet-restart
babylonnet-restart:
	@$(call print,h3,"restarting BabylonNet on port $(P) ...")
	@$(BABYLONNET_FILE) restart

.PHONY: babylonnet-status
babylonnet-status:
	@$(call print,h3,"BabylonNet status:")
	@$(BABYLONNET_FILE) status

.PHONY: babylonnet-stop
babylonnet-stop:
	@$(call print,h3,"stopping BabylonNet ...")
	@$(BABYLONNET_FILE) stop
	@$(call print,h3,"... BabylonNet stopped")

.PHONY: babylonnet-test
babylonnet-test: C:=
babylonnet-test: S:=
babylonnet-test: V:=
babylonnet-test:
	@$(call print,h3,"testing contract on BabylonNet ...")
	@$(BABYLONNET_FILE) client run script container:src/contracts/$(C)/$(C).tz on storage $(S) and input $(V)
	@$(call print,h3,"... complete")

.PHONY: babylonnet-typecheck
babylonnet-typecheck: C:=
babylonnet-typecheck:
	@$(call print,h3,"type checking contract on BabylonNet ...")
	@$(BABYLONNET_FILE) client typecheck script container:src/contracts/$(C)/$(C).tz -details
	@$(call print,h3,"... complete")

.PHONY: babylonnet-addresses
babylonnet-addresses:
	@$(call print,h3,"listing known addresses on BabylonNet ...")
	@$(BABYLONNET_FILE) client list known addresses
	@$(call print,h3,"... complete")

.PHONY: babylonnet-contracts
babylonnet-contracts: C:=
babylonnet-contracts:
ifeq ("$(C)","")
	@$(call print,h3,"listing known contracts on BabylonNet ...")
	@$(BABYLONNET_FILE) client list known contracts
else
	@$(call print,h3,"showing known contract $(C) on BabylonNet ...")
	@$(call print,h3,"balance:")
	@$(BABYLONNET_FILE) client get balance for $(C)
	@$(call print,h3,"storage:")
	@$(BABYLONNET_FILE) client get contract storage for $(C)
endif
	@$(call print,h3,"... complete")

.PHONY: babylonnet-deploy
babylonnet-deploy: C:=
babylonnet-deploy: A:=
babylonnet-deploy: S:=
babylonnet-deploy: B:=1.0
babylonnet-deploy:
	@$(call print,h3,"deployment contract $(C) to BabylonNet ...")
	@$(BABYLONNET_FILE) client originate contract $(C) transferring 0.1 from $(A) running container:src/contracts/$(C)/$(C).tz --init '$(S)' --burn-cap $(B)
	@$(call print,h3,"... complete")

.PHONY: babylonnet-call
babylonnet-call: C:=
babylonnet-call: A:=
babylonnet-call: I:=
babylonnet-call: F:=0
babylonnet-call: B:=1.0
babylonnet-call: D:=false
babylonnet-call:
ifeq ("$(D)","true")
	@$(call print,h3,"dry-run calling deployed BabylonNet contract $(C) with $(I) using account $(A)...")
	@$(BABYLONNET_FILE) client transfer $(F) from $(A) to $(C) -arg '$(I)' -D
else
	@$(call print,h3,"calling deployed BabylonNet contract $(C) with $(I) using account $(A)...")
	@$(BABYLONNET_FILE) client transfer $(F) from $(A) to $(C) -arg '$(I)' --burn-cap $(B)
endif
	@$(call print,h3,"... complete")

.PHONY: babylonnet-compare-sync
babylonnet-compare-sync:
	@$(call print,h3,"comparing BabylonNet last sync timestamp with current timestamp ...")
	@$(BABYLONNET_FILE) client get timestamp && date -u +"%Y-%m-%dT%H:%M:%SZ"
