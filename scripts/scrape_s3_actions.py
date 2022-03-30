import re
import pprint as pp

def get_test_actions(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    results = {}

    function_defs = re.split(r'\ndef ', text)
    # print(len(function_defs))
    # print(function_defs[len(function_defs)-1])

    # test names are always functions prefixed with "test_"
    test_name_pattern = re.compile("(test_.+)\(.*\):\n")

    # boto(3) API clients are named (.*)client(.*) in the test files
    s3_client_pattern = re.compile("[^\s]*client\.([^\(\),\s]+)[\(\),\n]*")
    for d in function_defs:
        m = re.search(test_name_pattern, d)
        if m:
            # print(m.group(1))
            actions = set(re.findall(s3_client_pattern, d))
            if len(actions) == 0:
                # print("N/A")
                results[m.group(1)] = "N/A"
            else:
                # print(actions)
                results[m.group(1)] = str(actions)

    return results

if __name__ == "__main__":
    results = get_test_actions("/Users/czhu/src/github/ceph-s3-tests/s3tests_boto3/functional/test_s3.py")
    pp.pprint(results)
