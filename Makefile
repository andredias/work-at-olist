.PHONY: install run test


install:
	pip install pip -U
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
	source $HOME/.poetry/env
	poetry install

	echo "SECRET_KEY='$(</dev/urandom tr -dc 'A-Za-z0-9@#$%&_+=!?,.*' | head -c 32)'
	FLASK_ENV=development
	FLASK_APP=olist
	" > .env

	poetry run flask deploy


run:
	poetry run flask run


test:
	poetry run pytest --cov-report term-missing --cov app/ -v --disable-warnings
