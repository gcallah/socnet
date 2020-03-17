# This shell script runs the SOCNET API server.
# The user_type env var is needed to make user interactions within
# SOCNET behave properly.
cd ..
export user_type="api"
export PYTHONPATH="$PWD"
python3 APIServer/api_endpoints.py
