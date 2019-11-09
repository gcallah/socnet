# SOCNET API server
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
from APIServer.form_api import get_form
from APIServer.data_store import read_alert, write_alert, db_init

app = Flask(__name__)
CORS(app)
api = Api(app)

form_field = api.model('form', {'form_name': fields.String('Model Name.')})


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/form')
class MessageFormat(Resource):
    def get(self):
        return get_form()


@api.route('/alert/<int:key>/')
class Alert(Resource):
    def get(self, key):
        return read_alert(key)

    def put(self, key):
        if read_alert(key) == 'No record found!':
            msg = request.json
            write_alert(msg, key)
            return_msg = 'Put key ' + str(key) + ' into DB... Success!'
        else:
            return_msg = 'Key ' + str(key) + ' already exists!'
        return return_msg


if __name__ == '__main__':
    db_init()
    app.run(host="0.0.0.0", port=8000, debug=True)
