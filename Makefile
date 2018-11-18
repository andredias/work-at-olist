.PHONY: install run test

SHELL := /bin/bash

install:
	pip install pipenv
	pipenv install
	pipenv install --dev

	echo "SECRET_KEY='$(</dev/urandom tr -dc 'A-Za-z0-9@#$%&_+=!?,.*' | head -c 32)'
	FLASK_ENV=development
	FLASK_APP=olist
	" > .env

	pipenv run flask deploy


run:
	pipenv run flask run


test:
	pipenv run pytest --cov-report term-missing --cov app/ -v --disable-warnings
