
# NOTE: use Python compatible with version 3.11

SHELL := /bin/bash
PYTHON := /usr/bin/python3
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

APP_UID := $(shell id -u)
APP_GID := $(shell id -g)
export APP_UID
export APP_GID

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(ACTIVATE) && pip install -r requirements.txt

clean:
	rm -rf $(VENV)

dev:
	mkdir -p var
	$(ACTIVATE) && fastapi dev app/main.py

run:
	$(ACTIVATE) && uvicorn app.main:app --no-access-log

build-image:
	docker build -t pyurls .

up:
	APP_UID=$(APP_UID) APP_GID=$(APP_GID) docker compose up -d

down:
	docker compose down


.PHONY: clean dev venv install image run up down
