from healthtogo.api.base import H2gResourceView

from storage.models import Nutritionist

class NutritionistList(H2gResourceView):
    _name = 'nutritionist_asd_api'
    _uri = "/apy/nutritionists"

    def get(self):
        groups_query = self.session.query(
            Nutritionist
        )
        return '', 200

# class Nutritionist(H2gResourceView):
#     _name = 'nutritionist_api'
#     _uri = "/apy/nutritionist/<str:organization_id>"

#     def __init__(self):
#         super().__init__()

#     def get(self):
#         return {'result': 'OK'}
