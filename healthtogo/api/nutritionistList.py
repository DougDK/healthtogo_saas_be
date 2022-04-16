from healthtogo.api.base import H2gResourceView

n = {
    "response":[
        {
            "name":"Douglas",
            "nutritionist_id":"douglas_costa_rossi",
            "lastName":"Costa Rossi",
            "CRN":"CRN1-119",
            "city":"Curitiba",
            "state":"Paraná",
            "expertise":"Alguma Coisa",
            "description":"TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO",
            "price":200.00,
            "socialMedia":"https://www.instagram.com/douglas.crossi/",
            "image":""
        },
        {
            "name":"Ricardo",
            "nutritionist_id":"ricardo_brugnari",
            "lastName":"Brugnari",
            "CRN":"CRN1-220",
            "city":"Curitiba",
            "state":"Paraná",
            "expertise":"Alguma Coisa",
            "description":"TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO",
            "price":144.00,
            "socialMedia":"https://www.instagram.com/ricardo.brugnari/",
            "image":""
        },
        {
            "name":"Emerson",
            "nutritionist_id":"emerson_schindler_jr",
            "lastName":"Schindler Junior",
            "CRN":"CRN1-338",
            "city":"Curitiba",
            "state":"Paraná",
            "expertise":"Alguma Coisa",
            "description":"TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXO TTEXTO TEXTO TEXTO TEXTO TEXTO TEXTO TEXTO",
            "price":340.00,
            "socialMedia":"https://www.instagram.com/emersonschindlerjr/",
            "image":""
        }
    ]
}

class NutritionistList(H2gResourceView):
    _name = 'nutritionist_list_api'
    _uri = "/apy/nutritionists"

    def get(self):
        return n, 200
