from healthtogo.api.nutritionistList import NutritionistList
from healthtogo.api.nutritionist import Nutritionist, NutritionistNoId
from healthtogo.api.login import LogIn
from healthtogo.api.base import register_endpoint


def register(app):

    # Create api endpoints.
    register_endpoint(app, LogIn)
    register_endpoint(app, NutritionistList)
    register_endpoint(app, Nutritionist)
    register_endpoint(app, NutritionistNoId)

    @app.errorhandler(404)
    def not_found(_):  # noqa: W0612 # pylint: disable=unused-variable
        return {"error": "Resource not found."}, 404

    return app
