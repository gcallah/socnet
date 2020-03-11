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
echo "Going to reboot the webserver"
touch  /var/www/socnet_pythonanywhere_com_wsgi.py
