PY=python3
PIP=pip3
APP=app.main:app

.PHONY: install install-all dev run test lint

install:
	$(PIP) install -r requirements.txt

install-all: install
	$(PIP) install -r requirements-optional.txt || true

run:
	$(PY) -m flask --app app.main --debug run --host 0.0.0.0 --port 8000

serve:
	$(PY) -m waitress --listen=0.0.0.0:8000 app.main:app

test:
	$(PY) -m pytest -q