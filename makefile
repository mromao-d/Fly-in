# Makefile Fly-in

SYS_PYTHON := python3
ENV_PIP := .venv/bin/pip

UV := .venv/bin/uv
MYPY := $(UV) run mypy
FLAKE8 := $(UV) run flake8
MYPY_FLAGS := --warn-return-any --warn-unused-ignores \
			  --ignore-missing-imports --disallow-untyped-defs \
			  --check-untyped-defs

install:
	@echo Preparing environment
	python3 -m venv .venv
	$(ENV_PIP) install uv
	$(UV) sync --no-dev

start: install
	$(UV) run main.py

run:
	$(UV) run main.py

debug:
	$(UV) python3 -m pdb fly-in.py

clean:
	@echo Cleaning environment ...
	rm -rf .venv $$(find . -name __pycache__ -o -name .mypy_cache)

clean-all: clean
	@echo Cleaning environment ...
	rm -rf solution
	rm -rf maps
	rm uv.lock

lint:
	@echo Lint tests ...
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . $(MYPY_FLAGS)

lint-strict:
	@echo Lint-strict tests ...
	$(FLAKE8) . --exclude=.venv
	$(MYPY) . --strict

re: clean install

.PHONY: install start run debug clean lint lint-strict re
