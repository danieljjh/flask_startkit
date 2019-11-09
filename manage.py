# -*- coding: utf-8 -*-
"""
manage.py  
- provides a command line utility for interacting with the
  application to perform interactive debugging and setup
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import MetaData
from myapp import create_app, db

# from app.application import create_app
# from model.models import db


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)

app = create_app()

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

# provide a migration utility command
manager.add_command('db', MigrateCommand)

# enable python shell with application context


@manager.shell
def shell_ctx():
    return dict(app=app,
                db=db,
                )


if __name__ == '__main__':
    manager.run()
