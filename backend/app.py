from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.message import MessageApiHandler
from api.data import DataApiHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return "<p>Hello, World!</p>"

api.add_resource(MessageApiHandler, '/message')

api.add_resource(DataApiHandler, '/data')