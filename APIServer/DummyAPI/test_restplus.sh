#!/bin/bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT
python api_restplus.py &
sleep 3

URL=http://127.0.0.1:5000

echo
KEY=$RANDOM
RECORD="'{\"Date\" : \"201801129\", \"Time\" : \"12:32\",\"Type\" : \"C\", \"Location\" : \"NYC\", \"Text\" : \"Hello ${KEY}!\",\"Who\" : \"xyz\",\"Org\" : \"NYU\"}'"
PutCommand="curl -X PUT ${URL}/alert/$KEY/ -H 'Content-Type: application/json' -d ${RECORD}"
echo Test PUT API
echo curl command is: $PutCommand
eval $PutCommand
echo
echo

echo Test GET API
GetCommand="curl -X GET ${URL}/alert/$KEY/"
echo curl command is: $GetCommand
eval $GetCommand
echo

