The .env does not work i Heroku.
It is necessary to set this environment variables instead:

FLASK_APP=olist
FLASK_ENV=development
SECRET_KEY='56tG?fcEVO!&tq9F45r!(?*CnVg8(E.b'

SECRET_KEY should be replaced by another random value.
