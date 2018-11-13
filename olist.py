from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent / '.env'
if dotenv_path.is_file():
    load_dotenv(str(dotenv_path))

import os  # noqa: E402
from flask_migrate import Migrate, upgrade  # noqa: E402
from app import create_app, db  # noqa: E402

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    if 'sqlite://' in app.config['SQLALCHEMY_DATABASE_URI']:
        # SQLite doesn't handle well with upgrade
        path = Path(app.config['SQLALCHEMY_DATABASE_URI'][10:])
        if path.is_file():
            path.unlink()
        db.create_all()
    else:
        # migrate database to latest revision
        upgrade()

    # insert sample data
    # this is part of olist's original requirements
    from app.models import Call
    source = '99988526423'
    destination = '9933468278'
    data = (
        (70, datetime(2016, 2, 29, 12, 0, 0), datetime(2016, 2, 29, 14, 0, 0)),
        (71, datetime(2017, 12, 11, 15, 7, 13), datetime(2017, 12, 11, 15, 14, 56)),
        (72, datetime(2017, 12, 12, 22, 47, 56), datetime(2017, 12, 12, 22, 50, 56)),
        (73, datetime(2017, 12, 12, 21, 57, 13), datetime(2017, 12, 12, 22, 10, 56)),
        (74, datetime(2017, 12, 12, 4, 57, 13), datetime(2017, 12, 12, 6, 10, 56)),
        (75, datetime(2017, 12, 13, 21, 57, 13), datetime(2017, 12, 14, 22, 10, 56)),
        (76, datetime(2017, 12, 12, 15, 7, 58), datetime(2017, 12, 12, 15, 12, 56)),
        (77, datetime(2018, 2, 28, 21, 57, 13), datetime(2018, 3, 1, 22, 10, 56)),
    )
    # bulk insert
    # ref: https://docs.sqlalchemy.org/en/latest/_modules/examples/performance/bulk_inserts.html
    db.session.add_all(
        Call(id=v[0], source=source, destination=destination, start_timestamp=v[1],
             end_timestamp=v[2]) for v in data
    )
    db.session.flush()
    db.session.commit()

    # ensure all users are following themselves
    # User.add_self_follows()
