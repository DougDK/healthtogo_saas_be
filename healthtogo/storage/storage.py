# from contextlib import contextmanager
# import logging
# import os

# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy.engine import Engine
# from sqlalchemy import MetaData, Table, Column, Integer, String
# from flask import current_app

# from healthtogo.core.healthtogo_sqlalchemy import HealthToGoSQLAlchemy
# from flask_sqlalchemy import SignallingSession

# main Flask-SQLAlchemy object - as yet unbound to a Flask app
# the class_ kwarg defines the default Session class used when creating sessions.
# db = HealthToGoSQLAlchemy(session_options={'class_': SignallingSession})

# """ Storage contains various functions for logical DB operations. The DB calls contained in these functions are managed
# in scoped sessions defined by either a wrapper or a context provided below."""


# # This global is a scoped SQLAlchemy session as provided by Flask-SQLAlchemy. it is also
# # accessible in other ways, but this is how the original codebase and the decorators below
# # access it.
# OuterScope_Session = db.session


# @contextmanager
# def session_scope():
#     """Provide a transactional scope around a series of operations.
#     This is gives a specific scope to API calls or any code that bound some number of related DB operations.
#     Can be used anywhere a related set of DB session calls are made. (Intended for use in the calling code.)"""
#     # TODO: should we call this or not? `db.session` is just the session, whereas `db.session()` is a SignalingSession
#     #
#     # more context: db.session is a scoped_session object which proxies to the 'actual' session when appropriate.
#     #   so using db.session gives extra methods, like remove(). but a session method like commit(),
#     #   close(), etc when called from db.session goes to the same object in memory as when using db.session().
#     #
#     # In [1]: db.session
#     # Out[1]: <sqlalchemy.orm.scoping.scoped_session at 0x104563a90>
#     #
#     # In [2]: db.session()
#     # Out[2]: <sqlalchemy.orm.session.SignallingSession at 0x1067f4f60>

#     session: Session = db.session()
#     try:
#         yield session
#         session.commit()
#     except Exception as err:  # noqa: W0703
#         logging.exception("Something broke...", exc_info=err)
#         capture_exception(err)
#         session.rollback()

#         raise err
#     finally:
#         # TODO(db): if we don't need this in prod, remove the finally clause
#         if not current_app.testing:
#             session.close()


# def session_scoper(the_func):
#     """ Provides a wrapper for a scope that represents a logical unit of work.
#     This is gives scope to code that bounds session calls doesn't call them directly.
#     (Intended for use in the calling code.)"""
#     def wrapper(*args, **kwargs):
#         with session_scope():
#             return the_func(*args, **kwargs)
#     return wrapper


# def reflect_db(config):
#     return setup_db(config)['outerscope_session']


# def setup_db(config):  # noqa: W0613 # pylint: disable=unused-argument
#     """Create the DB engine and backwards-compat globals"""
#     global OuterScope_Session  # noqa: W0603 # pylint: disable=global-statement

#     # counting on the flask-sqlalchemy created engine
#     engine = db.engine

#     OuterScope_Session = db.session

#     return {'engine': engine,
#             'outerscope_session': OuterScope_Session}


# _base = None


# def get_base():
#     global _base  # noqa: W0603 # pylint: disable=global-statement
#     # only need to do this once per process
#     if _base is None:
#         meta = MetaData(bind=db.engine)
#         meta.reflect(db.engine, views=True)

#         # associate primary keys with the views so they can be automapped
#         Table('recommendation_get_view', meta,
#               Column('recommendation_id', Integer, primary_key=True),
#               autoload=True, autoload_with=db.engine, extend_existing=True)

#         Table('plant_opportunity', meta,
#               Column('organization_id', Integer, primary_key=True),
#               Column('catalog_id', Integer, primary_key=True),
#               Column('plant_id', String(255), primary_key=True),
#               autoload=True, autoload_with=db.engine, extend_existing=True)

#         Table('plant_material_current', meta,
#               Column('organization_id', Integer, primary_key=True),
#               Column('catalog_id', Integer, primary_key=True),
#               Column('material_id', String(255), primary_key=True),
#               Column('plant_id', String(255), primary_key=True),
#               autoload=True, autoload_with=db.engine, extend_existing=True)

#         _base = automap_base(metadata=meta)
#         _base.prepare(db.engine)
#     return _base


# def reset_pool_after_fork() -> None:
#     """
#     Reset the SQLAlchemy connection pool after a fork (for Celery or Multiprocessing/Billiard).
#     Note that this will close connections in both the parent and children, so it is only safe
#     *before* the pool has been used at all. To be safe, also call engine.dispose() and
#     engine.connect() in the parent!

#     See GPI-728
#     :return: None
#     """
#     logging.debug("Resetting pool in process: %d", os.getpid())
#     engine: Engine = db.engine
#     if engine.pool.checkedout() > 0:
#         logging.warning("SQLAlchemy pool has %d checked out connections", engine.pool.checkedout())
#     engine.dispose()
#     engine.connect()
#     engine.scalar("SELECT 1;")
