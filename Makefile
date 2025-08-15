
# NOTE: assume system Python is compatible with version 3.11

SHELL := /bin/bash
PYTHON := /usr/bin/python3
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(ACTIVATE) && pip install -r requirements.txt

clean:
	rm -rf $(VENV)


dev:
	$(ACTIVATE) && fastapi dev app/main.py
#	uv run uvicorn app.main:app --reload
#   python3 -m app.main

run:
	$(ACTIVATE) && uvicorn app.main:app --no-access-log

build-image:
	docker build -t pyurls .

up:
	docker compose up -d

down:
	docker compose down




.PHONY: clean dev venv install image run up down
