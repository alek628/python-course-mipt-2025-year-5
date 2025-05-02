all: list-targets

.PHONY: all list-targets venv
list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]'

setup: venv deps

venv:
	python3.11 -m venv ./venv/

deps:
	. venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate

run:
	docker compose up

run-local:
	. venv/bin/activate && \
		fastapi run --reload src/main.py && \
		deactivate

lint:
	echo tbd

tests:
	echo tbd

link:
	echo tbd