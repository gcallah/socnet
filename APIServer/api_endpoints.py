# SOCNET API server
from flask import Flask
from flask_restplus import Resource, Api
from flask_cors import CORS
from APIServer.form_api import get_form


app = Flask(__name__)
CORS(app)
api = Api(app)

# user = APIUser("Dennis", None)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/APIServer')
class MessageFormat(Resource):
    def get(self, form_name):
        return get_form(form_name)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
