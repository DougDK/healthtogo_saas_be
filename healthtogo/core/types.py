from sqlalchemy.orm import Session
from flask import Flask

from healthtogo.storage import db


class H2GApp(Flask):
    @staticmethod
    def session() -> Session:
        return db.session()
    def _get_current_object(self) -> 'H2GApp':
        return self
