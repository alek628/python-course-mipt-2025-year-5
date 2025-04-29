all: list-targets

.PHONY: all list-targets venv
list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]'

setup: venv dep

venv:
	python3.11 -m venv ./venv/

deps:
	. venv/bin/activate && \
		pip install -r requirements.txt && \
		deactivate

run:
	echo tbd

lint:
	echo tbd

tests:
	echo tbd

link:
	echo tbd