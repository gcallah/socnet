from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions

import json

app = FlaskAPI(__name__)

@app.route("/echo", methods=['POST'])
def echo_test():
    """
    Echoes back input text 
    """
    text = str(request.data.get('text', ''))
    return text, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=True)

