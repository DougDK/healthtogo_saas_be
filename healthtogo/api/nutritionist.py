from healthtogo.api.base import H2gResourceView
from .nutritionistList import n
from flask import request

class Nutritionist(H2gResourceView):
    _name = 'nutritionist_api'
    _uri = "/apy/nutritionist/<string:nutritionist_id>"

    def __init__(self):
        super().__init__()

    def get(self, nutritionist_id):
        for nutri in n['response']:
            if nutri["nutritionist_id"]==nutritionist_id:
                return nutri
        return '', 404

    def delete(self, nutritionist_id):
        for nutri in n['response']:
            if nutri["nutritionist_id"]==nutritionist_id:
                n['response'].remove(nutri)
                return '', 200
        return '', 404
    
    def put(self, nutritionist_id):
        request_data = request.get_json(self)
        return {'result': 'OK'}

class NutritionistNoId(H2gResourceView):
    _name = 'nutritionist_noid_api'
    _uri = "/apy/nutritionist"

    def __init__(self):
        super().__init__()

    def post(self):
        request_data = request.get_json(self)
        request_data['nutritionist_id']="{} {}".format(request_data["name"], request_data["lastName"]).replace(" ","_").lower()
        request_data['image']=""
        n['response'].append(request_data)
        return {'result': 'OK'}
