from flask import Flask, request
from flask_restplus import Resource, Api
from doc_process import *

app = Flask(__name__)
api = Api(app)

@api.route('/alert/<int:key>/')
class Alert(Resource):
    def get(self, key):
        return readFile(key)
    def put(self, key):
        if readFile(key) == 'No record found!':
            msg = request.json
            writeToFile(msg, key)
            return_msg = 'Put key ' + str(key) + ' into DB... Success!'
        else:
            return_msg = 'Key ' + str(key) + ' already exists!' 
        return return_msg

if __name__ == '__main__':
    docInit()
    app.run()

