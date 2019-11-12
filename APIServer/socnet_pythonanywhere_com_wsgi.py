import sys

# add your project directory to the sys.path
project_home = u'/home/socnet/socnet/APIServer'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from api_endpoints import app as application  # noqa
