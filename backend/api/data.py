from flask_restful import Api, Resource
from flask import request
from utils.helper import get_data

class DataApiHandler(Resource):

    def get(self):
        print(request.args.get("dining"))
        get_data(request.args.get("dining"))
        return ('', 204)
