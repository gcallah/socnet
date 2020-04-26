export user_type="test"
export test_dir="tests"
export ignore_files="scheduler"  # dummy file!
export ignore_dir="utils"

cd ..
export PYTHONPATH=$PWD

if [ -z $1 ]
then
    export capture=""
else
    export capture="--nocapture"
fi

echo "SOCNET_HOME: $SOCNET_HOME"
nosetests --ignore-files=$ignore_files --exe --verbose --with-coverage --cover-package=APIServer $capture --exclude=$ignore_dir
