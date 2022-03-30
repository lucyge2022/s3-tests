from xml.etree import ElementTree
import pandas as pd
from scrape_s3_actions import *

ceph_s3_tests_dir="../s3tests_boto3/functional"
test_data_dir="../data"

if __name__ == "__main__":
    nosetests = ["test_s3"]

    for nosetest in nosetests:
        actions = get_test_actions("%s/%s.py" % (ceph_s3_tests_dir, nosetest))

        cols = ["classname", "testname", "result", "message", "stacktrace", "api actions"]
        rows = []

        xml = ElementTree.parse("%s/%s.xml" % (test_data_dir, nosetest))
        testsuite = xml.getroot()
        for testcase in testsuite:
            testname = testcase.attrib['name']
            result = 'pass'
            msg = ''
            trace = ''

            print("%s ... " % testname, end='')
            if testcase.find('error') is not None:
                # error takes precedence over failures
                result = 'error'
                msg = testcase.find('error').attrib['message']
                trace = testcase.find('error').text
            elif testcase.find('failure') is not None:
                result = 'fail'
                msg = testcase.find('failure').attrib['message']
                trace = testcase.find('failure').text
            print(result)
            try:
                test_actions = actions[testname]
            except KeyError:
                test_actions = "N/A"
            rows.append({cols[0]: testcase.attrib['classname'],
                cols[1]: testname,
                cols[2]: result,
                cols[3]: msg,
                cols[4]: trace,
                cols[5]: test_actions})

        df = pd.DataFrame(rows, columns=cols)
        df.to_csv("%s/%s.csv" % (test_data_dir, nosetest))

        print("Tests: %s" % testsuite.attrib['tests'])
        print("Errors: %s" % testsuite.attrib['errors'])
        print("Failures: %s" % testsuite.attrib['failures'])
        print("Skipped: %s" % testsuite.attrib['skip'])
