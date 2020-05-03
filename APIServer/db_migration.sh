# This shell script do database migration on Pythonanywhere server

git pull origin master
source /home/socnet/.virtualenvs/socnet/bin/activate

export FLASK_APP=api_endpoints.py

# Then modify model.py. After that, run db_migration2.sh 