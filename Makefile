.PHONY: install run test env

SECRET_KEY := $(shell cat /dev/urandom | tr -dc 'A-Za-z0-9@$%&_+=!?,.*[]()' | head -c 32)

env:
	echo "SECRET_KEY='$(SECRET_KEY)'\n\
	FLASK_ENV=development\n\
	FLASK_APP=olist\n\
	" > .env


install: env
	pip install pipenv
	pipenv install
	pipenv install --dev
	pipenv run flask deploy


run:
	pipenv run flask run


test:
	pipenv run pytest --cov-report term-missing --cov app/ -v --disable-warnings
