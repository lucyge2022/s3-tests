#! /bin/bash

# Run this script from the root-directory of the repo

# nosetests has the following flag:
#   --debug-log=FILE  Log debug messages to this file (default: sys.stderr)
# however it doesn't seem to be respected for some reason; so for now we are stuck with all logs going to stdout

NOSETESTS="${1:-test_s3}"
CONF_FILE="${2:-s3tests.conf.SAMPLE}"

for test in ${NOSETESTS}; do
	echo "Running nosetest on s3tests_boto3.functional.${test}"

	S3TEST_CONF="${CONF_FILE}" ./virtualenv/bin/nosetests \
		--logging-clear-handlers \
		--nologcapture \
		-q \
		--verbosity=2 \
		--with-xunit \
		--xunit-file="data/${test}.xml" \
		"s3tests_boto3.functional.${test}" 2>&1 | tee "data/${test}.out"
done
