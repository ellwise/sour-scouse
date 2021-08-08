delete:
	chalice delete

deploy:
	chalice deploy

format:
	python -m black --config pyproject.toml .

install:
	pip install pip-tools
	pip-compile requirements.in
	pip install -r requirements.txt

lint:
	python -m flake8 --config setup.cfg
	python -m black  --config pyproject.toml --check .

run:
	chalice local

venv:
	python -m venv venv
