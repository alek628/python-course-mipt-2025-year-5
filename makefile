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
	docker compose up --build

run-local:
	. venv/bin/activate && \
		fastapi run --reload src/main.py && \
		deactivate

generate-secret:
	echo >> .env
	echo -n "secret_key="
	hexdump -vn32 -e'4/4 "%08x" 1 ""' /dev/urandom >> .env
	echo >> .env

clean:
	docker rm python-course-mipt-2025-year-5-db-1 python-course-mipt-2025-year-5-web-1 || true
	docker volume rm python-course-mipt-2025-year-5_postgres_data || true

lint:
	. venv/bin/activate && \
		pylint src/ | tee /dev/tty > pylint.txt && \
		deactivate