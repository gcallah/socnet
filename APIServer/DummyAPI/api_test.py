from flask import request  
from flask_api import FlaskAPI, status, exceptions

import os

app = FlaskAPI(__name__)

DB_TEMP = 'db_temp'
def writeToFile(msg, key):
    f = open(DB_TEMP, 'a')
    msg_str = 'Record ' + str(key) + ' : ' + 'Date ' + msg.get('Date', '') + '|' \
                              + 'Time ' + msg.get('Time', '') + '|' \
                              + 'Type ' + msg.get('Type', '') + '|' \
                              + 'Location ' + msg.get('Location', '') + '|' \
                              + 'Text ' + msg.get('Text', '') + '|' \
                              + 'Who ' + msg.get('Who', '') + '|' \
                              + 'Org ' + msg.get('Org', '') + '\n' 
    f.write(msg_str)
    f.close()
    return

def readFile(key):
    f = open(DB_TEMP, 'r')
    for line in f:
        num = line.split(' ')[1]
        if int(num) == key:
            return line
    return 'No record found!'

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
    if not os.path.isfile(DB_TEMP):
       open(DB_TEMP, 'w+')
    app.run(debug=True)

