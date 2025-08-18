
# NOTE: use Python compatible with version 3.11

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
	mkdir -p var
	$(ACTIVATE) && fastapi dev app/main.py

run:
	$(ACTIVATE) && uvicorn app.main:app --no-access-log

build-image:
	docker build -t pyurls .

run-image:
	docker run -it -p "8000:8000" pyurls

up: build-image
	docker compose up -d

down:
	docker compose down

remove-volume:
	docker volume rm pyurls_var -f


.PHONY: clean dev venv install image run up down
