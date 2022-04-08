from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm


class HealthToGoSQLAlchemy(SQLAlchemy):
    """
    In order to use a subclassed Session object with Flask-SQLAlchemy, we must subclass the flask_sqlalchemy.SQLAlchemy object
    and override the create_session method. This is because that method does
     "return orm.sessionmaker(class_=SignallingSession, db=self, **options)"
    i.e., has hardcoded "class_" kwarg, but we want that kwarg to be taken from the options.
    """

    def create_session(self, options):
        return orm.sessionmaker(db=self, **options)
