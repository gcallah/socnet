# This shell script runs the SOCNET API server.
# The user_type env var is needed to make user interactions within
# SOCNET behave properly.
export user_type="api"
python3 api_endpoints.py
