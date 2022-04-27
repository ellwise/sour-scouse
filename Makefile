format:
	python -m black --config pyproject.toml .

lint:
	python -m flake8 --config setup.cfg
	python -m black  --config pyproject.toml --check .

run:
	python app.py

gunicorn:
	gunicorn -w 1 app:server

venv:
	python -m venv venv
