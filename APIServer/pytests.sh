export user_type="test"
export test_dir="tests"
export ignores="scheduler"  # dummy file!

export PYTHONPATH=$PWD

if [ -z $1 ]
then
    export capture=""
else
    export capture="--nocapture"
fi

echo "SOCNET_HOME: $SOCNET_HOME"
nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=APIServer $capture
