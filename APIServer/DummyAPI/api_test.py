from flask import request  
from flask_api import FlaskAPI, status, exceptions
from doc_process import *

import os

app = FlaskAPI(__name__)

DB_TEMP = 'db_temp'

@app.route("/echo", methods=['POST'])
def echo_test():
    """
    Echoes back input text 
    """
    text = str(request.data.get('text', ''))
    return text, status.HTTP_200_OK

@app.route("/messages/<int:key>/", methods=['GET', 'PUT'])
def simple_message(key):
    """
    GET or PUT messages
    """
    if request.method == 'PUT':
        if readFile(key) == 'No record found!':
            msg = request.data
            writeToFile(msg, key)
            return_msg = 'Put key ' + str(key) + ' into DB... Success!' 
        else:
            return_msg = 'Key ' + str(key) + ' already exists!' 
        return return_msg, status.HTTP_200_OK
    
    #request.method == 'GET'
    return readFile(key), status.HTTP_200_OK

if __name__ == "__main__":
    docInit()
    app.run(debug=True)

