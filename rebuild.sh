#!/bin/bash
# This runs on the production server: fetches new code,
# installs needed packages, and restarts the server.

export project_name=socnet

# get new source code onto the server
git pull origin master
# activate our virtual env:
source /home/$project_name/.virtualenvs/$project_name/bin/activate
# install all of our packages:
pip install -r requirements/requirements.txt
# check and install if pa_reload_webapp.py does not exist
FILE=pa_reload_webapp.py
if [ -f "$FILE" ]; then
    echo "$FILE exist"
else 
    echo "$FILE does not exist"
    pip3.5 install --user pythonanywhere
fi
API_TOKEN=$1 pa_reload_webapp.py $project_name.pythonanywhere.com
# the next line gives us evidence as to whether script ran on PA:
touch reboot
