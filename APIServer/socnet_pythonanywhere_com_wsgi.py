# This file is a backup of WSGI configuration required to serve up the
# web application at http://socnet.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.


import sys

# add your project directory to the sys.path
project_home = u'/home/socnet/socnet'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from APIServer.api_endpoints import app as application  # noqa
