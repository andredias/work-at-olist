from pathlib import Path
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
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    # Role.insert_roles()

    # ensure all users are following themselves
    # User.add_self_follows()
