#!/bin/bash

# This is a script to test api_test.py

trap "exit" INT TERM ERR
trap "kill 0" EXIT
python api_test.py &
sleep 3

URL=http://127.0.0.1:5000

echo
echo Test echo API
if [ -n "$1" ]; then
    TEST_TEXT=$1
else
    RANDOM=$$
    TEST_TEXT="Thisisatest$RANDOM"
fi
TEXT="'{\"text\":\"$TEST_TEXT\"}'"
EchoCurl="curl -X POST -H 'Content-Type: application/json' -d ${TEXT} ${URL}/echo"
echo "Input text is: $TEST_TEXT"
echo curl command is: $EchoCurl
echo "Response message is..."
eval $EchoCurl
echo
echo

KEY=$RANDOM
RECORD="'{\"Date\" : \"201801129\", \"Time\" : \"12:32\",\"Type\" : \"C\", \"Location\" : \"NYC\", \"Text\" : \"Hello ${KEY}!\",\"Who\" : \"xyz\",\"Org\" : \"NYU\"}'"
PutCommand="curl -X PUT ${URL}/messages/$KEY/ -H 'Content-Type: application/json' -d ${RECORD}"
echo Test PUT API
echo curl command is: $PutCommand
eval $PutCommand
echo
echo

echo Test GET API
GetCommand="curl -X GET ${URL}/messages/$KEY/"
echo curl command is: $GetCommand
eval $GetCommand
echo
