import logging
from typing import Optional
import os


from flask import Flask
from flask.json import JSONEncoder
import decimal

# from tombstone.storage import storage, db
# from tombstone.core.config import Config
from healthtogo.core.types import H2GApp
# from tombstone.core.signals import user_authentication_succeeded
# import tombstone.tasks.celery as celery_mod
# from tombstone.core.cache import setup_cache
# import tombstone.core.ingest as ingest
# from tombstone.core.version import get_build_info, app_version
# import tombstone.core.metrics as tsmetrics
# from tombstone.web.logging import setup_logging

# import tombstone.commands as commands

os.environ['TZ'] = 'UTC'


def create_base_app(name=__name__,  override_config: Optional[dict] = None) -> H2GApp:
    """Create the base Flask application to be shared between the web service and
    background worker. Has config, database, and commands setup, but not any blueprints or
    views or other web-related setup"""


    app = H2GApp(name)
    # load_config(app, override_config)
    # setup_logging(app)
    # commands.register_commands(app)
    # setup_db(app)
    # setup_observability(app)

    # setup_cache(app)

    # setup_celery(app)


    return app


# def load_config(app: Flask, override_config: Optional[dict]) -> None:
#     """Load configuration into app.config"""
#     # get app-wide defaults
#     app.config.from_object("tombstone.conf.default")

#     config = Config(app=app)
#     config_data = config.read()

#     if override_config:
#         config_data.update(override_config)

#     app.config.update(config_data)


# def setup_db(app: TombstoneApp) -> None:
#     """Initialize database and setup backwards-compat global and app-scope variables"""
#     # DB setup
#     with app.app_context():
#         # https://github.com/jfinkels/flask-restless/issues/409
#         db.app = app
#         db.init_app(app)
#         app.db_bits = storage.setup_db(app.config)

#         # scoped db session
#         app.tombstone_db = db.session

#         # the SQLAlchemy wrapper
#         app.sqla = db


# def _set_sentry_user(sender, user_id=None, user_email=None, **kwargs):  # pylint: disable=unused-argument
#     """
#     Signal listener for user authentication events to populate Sentry user context
#     :param sender: sender of the signal
#     :param user_id: integer id of user
#     :param user_email: string email
#     :param kwargs: rest of signal args; ignored
#     :return:
#     """
#     with configure_scope() as scope:
#         scope.user = {"email": user_email, "id": user_id}


# ExceptionCounter = Counter("exceptions_sent_to_sentry", "counter of exceptions reported to Sentry")


# def before_sentry_send(event, _):
#     """Count exceptions sent to Sentry"""
#     ExceptionCounter.inc(1)
#     return event


# def setup_observability(app: TombstoneApp) -> None:
#     """Setup all logging, exception reporting, etc."""
#     logging.getLogger().setLevel("INFO")

#     add_metrics(app)

#     if app.config.get("SENTRY_DSN", None) and not app.testing:
#         enable_sentry(app, app.config.get("SENTRY_DSN"))

#     if 'ELASTIC_APM' in app.config and app.config.get('ELASTIC_APM_ENABLED', True):
#         os.environ['ELASTIC_APM_ENVIRONMENT'] = app.env
#         apm.init_app(app)


# def setup_celery(app: TombstoneApp) -> None:
#     return celery_mod.config_celery(celery_mod.celery, app)


# def add_metrics(app: TombstoneApp):
#     build_info = get_build_info()
#     # static information as metric
#     tsmetrics.metrics.info('app_info', 'Application Info',
#                            app=build_info.get('CI_PROJECT_NAME', 'tombstone'),
#                            version=app_version(),
#                            ci_commit_sha=build_info.get('CI_COMMIT_SHA'),
#                            ci_build_epoch=str(build_info.get('CI_BUILD_EPOCH')),
#                            ci_build_date=build_info.get('BUILD_DATE'))

#     app.metrics = tsmetrics.metrics

#     tsmetrics.metrics.init_app(app)


# def setup_boto(app: TombstoneApp) -> None:
#     if app.config.get('BOTO_USE_MFA_PROFILE'):
#         app.logger.info('Using MFA profile as default profile for boto3')  # pylint: disable-msg=E1101
#         boto3.setup_default_session(profile_name='mfa')
