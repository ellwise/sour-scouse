format:
	python -m black --config pyproject.toml .

lint:
	python -m flake8 --config setup.cfg
	python -m black  --config pyproject.toml --check .

venv:
	python -m venv venv
