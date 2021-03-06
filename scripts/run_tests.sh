#!/bin/bash
#
# Run project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

# Use default environment vars for localhost if not already set
export EQ_CLOUDWATCH_LOGGING=False

export EQ_RABBITMQ_ENABLED=False

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_ENABLE_CACHE" ]; then
  export EQ_ENABLE_CACHE=True
fi

echo "Environment variables in use:"
env | grep EQ_

set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

flake8 --max-complexity 10 --count
display_result $? 1 "Flake 8 code style check"

pylint --rcfile=.pylintrc -j 0 ./app ./tests
# pylint bit encodes the exit code to allow you to figure out which category has failed.
# https://docs.pylint.org/en/1.6.0/run.html#exit-codes
# http://stackoverflow.com/questions/6626351/how-to-extract-bits-from-return-code-number-in-bash
# We want to fail if there are any errors or fatal errors so we use 3
errorcode=$?
(( res = $errorcode & 3 ))
display_result $res "Pylint code style check"

py.test --cov=app --cov-report xml $@ $1
display_result $? 2 "Unit tests"

# Run front end tests
npm config set python python2.7

yarn test_unit_no_watch
display_result $? 1 "Front end unit tests"

if [ -z "$EQ_FUNCTIONAL_TEST_SUITES" ]; then
    export EQ_FUNCTIONAL_TEST_SUITES="core"
fi
echo "Running front end functional tests [${EQ_FUNCTIONAL_TEST_SUITES}]"
yarn test_functional -- --suite ${EQ_FUNCTIONAL_TEST_SUITES}

display_result $? 1 "Front end functional tests"
