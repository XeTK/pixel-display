from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from yaml import load

CONFIG_FILE = "config.yaml"

config_file = open(CONFIG_FILE, 'r')
config = load(config_file)

PORT = config['PORT']
DEBUG = config['DEBUG'] == "True"


class AlbumArt(Resource):
    def __init__(self, **kwargs):
        self.callback = kwargs['callback']
        self.auth_token = kwargs['auth_token']

    def get(self):
        return self.callback(self.auth_token)


def setup_rest_endpoint(callback, auth_token):
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(app)

    api.add_resource(
        AlbumArt,
        '/albumart',
        resource_class_kwargs={
            'callback': callback,
            'auth_token': auth_token
        }
    )

    app.run(debug=DEBUG, port=PORT)




