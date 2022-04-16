import inspect
from typing import Type

from flask.views import MethodView
from flask_httpauth import HTTPBasicAuth
# from healthtogo.core.healthtogo_session import H2GSession

auth = HTTPBasicAuth()

# supported possible methods
VERBS = ('get', 'post', 'delete', 'head', 'options', 'put', 'patch')

class H2gResourceView(MethodView):
    def __init__(self):
        # self.session: H2GSession = storage.db.session()
        return
    
    @classmethod
    def get_name(cls) -> str:
        return cls._name

    @classmethod
    def get_uri(cls) -> str:
        return cls._uri

def _filter_methods(subject):
    """
    Helper function that filters out functions in a view class that
    correspond to HTTP methods
    """
    return inspect.isfunction(subject) and subject.__name__ in VERBS

def register_endpoint(app, view_class: Type[H2gResourceView]):
    """
    Add a view class to the given flask app.
    """
    view_func = view_class.as_view(view_class.get_name())
    http_funcs = inspect.getmembers(view_class, _filter_methods)
    methods = [obj.__name__.upper() for _, obj in http_funcs]
    app.add_url_rule(view_class.get_uri(), view_func=view_func, methods=methods)