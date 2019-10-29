#!/bin/bash

URL=http://127.0.0.1:5000/echo

# Test echo API
if [ -n "$1" ]; then
    TEST_TEXT=$1
else
    RANDOM=$$
    TEST_TEXT="Thisisatest$RANDOM"
fi
TEXT="'{\"text\":\"$TEST_TEXT\"}'"
echo "Input text is: $TEST_TEXT"
echo "Response message is..." 
eval "curl -X POST -H \"Content-Type: application/json\" -d $TEXT $URL"
echo


