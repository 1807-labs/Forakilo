.DEFAULT_GOAL := lint

LINT_PATHS ?= service tests
MAX_LINE_LENGTH ?= 127
MAX_COMPLEXITY ?= 10

ifeq ($(OS),Windows_NT)
BASE_PYTHON ?= python
VENV_PYTHON := .venv/Scripts/python.exe
else
BASE_PYTHON ?= python3
VENV_PYTHON := .venv/bin/python
endif

PIP := $(VENV_PYTHON) -m pip
LINT_MARKER := .venv/.lint-tools-ready

.PHONY: help venv install lint-deps lint lint-critical pylint test check clean

help:
	@echo Available targets:
	@echo   make              Run the complete lint suite
	@echo   make lint         Run Flake8 and Pylint
	@echo   make lint-critical Run critical Flake8 checks only
	@echo   make pylint       Run Pylint only
	@echo   make install      Install project dependencies
	@echo   make test         Run the test suite
	@echo   make check        Run lint and tests
	@echo   make clean        Delete the local virtual environment

$(VENV_PYTHON):
	$(BASE_PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel

venv: $(VENV_PYTHON)

install: $(VENV_PYTHON)
	$(PIP) install -r requirements.txt

$(LINT_MARKER): $(VENV_PYTHON)
	$(PIP) install --upgrade flake8 pylint
	$(VENV_PYTHON) -c "from pathlib import Path; Path(r'$(LINT_MARKER)').touch()"

lint-deps: $(LINT_MARKER)

lint-critical: $(LINT_MARKER)
	$(VENV_PYTHON) -m flake8 $(LINT_PATHS) --count --select=E9,F63,F7,F82 --show-source --statistics

pylint: $(LINT_MARKER)
	$(VENV_PYTHON) -m pylint $(LINT_PATHS) --max-line-length=$(MAX_LINE_LENGTH)

lint: lint-critical
	$(VENV_PYTHON) -m flake8 $(LINT_PATHS) --count --max-complexity=$(MAX_COMPLEXITY) --max-line-length=$(MAX_LINE_LENGTH) --statistics
	$(VENV_PYTHON) -m pylint $(LINT_PATHS) --max-line-length=$(MAX_LINE_LENGTH)

test: $(VENV_PYTHON)
	$(VENV_PYTHON) -m pytest -v

check: lint test

clean:
	$(BASE_PYTHON) -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)"
