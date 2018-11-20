from flask import Flask, request
from flask_restful import Api, Resource, reqparse


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


class Callback(Resource):
    def __init__(self, **kwargs):
        self.callback = kwargs['callback']

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        parser.add_argument('state')
        args = parser.parse_args()

        if args['code'] is not None:
            auth_code = args['code']
            self.callback(auth_code)
            shutdown_server()
            return "Got what we needed."

        return args


def setup_return_endpoint(port, debug, callback):
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(
        Callback,
        '/callback',
        resource_class_kwargs={
            'callback': callback
        }
    )

    app.run(debug=debug, port=port)
