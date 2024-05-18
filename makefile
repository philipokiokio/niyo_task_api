

PYTHON = venv/bin/python
PIP = venv/bin/pip
BLACK = venv/bin/python -m black
RUFF = venv/bin/python -m ruff 
MESSAGE = "Local Table Migrations"
STEP = 1


venv : 
	python3 -m venv venv
	
get-permission :
	chmod +x makefile	

install :
	pip install -r requirements.txt 


local-migrate-init :
	alembic -c local_dev_alembic.ini init local_migration

local-migration:
	alembic -c local_dev_alembic.ini revision -m "$(MESSAGE)" --autogenerate


local-migrate:
	alembic -c local_dev_alembic.ini upgrade heads


local-migrate-down:
	alembic -c local_dev_alembic.ini downgrade -"$(STEP)"


local-head:
	alembic -c local_dev_alembic.ini heads

run-server:
	uvicorn task.root.app:app --reload --port=8000


format : 
	$(BLACK) --preview ./task

standard:
	$(RUFF) check ./task --ignore=E731,E712
