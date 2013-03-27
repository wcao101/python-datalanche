# -*- coding: utf-8 -*-

from datalanche import *
import json
import os
import sys

def is_boolean(s):
    if s == True or s == False:
        return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def is_string(s):
    return isinstance(s, basestring)

def convert_filter(value):
    left = None
    op = None
    right = None
    
    if 'left' in value:
        left = value['left']
    if 'op' in value:
        op = value['op']
        if op == 'and':             op = DLFilterOp.AND
        elif op == 'or':            op = DLFilterOp.OR
        elif op == 'eq':            op = DLFilterOp.EQ
        elif op == 'not_eq':        op = DLFilterOp.NOT_EQ
        elif op == 'gt':            op = DLFilterOp.GT
        elif op == 'gte':           op = DLFilterOp.GTE
        elif op == 'lt':            op = DLFilterOp.LT
        elif op == 'lte':           op = DLFilterOp.LTE
        elif op == 'in':            op = DLFilterOp.IN
        elif op == 'not_in':        op = DLFilterOp.NOT_IN
        elif op == 'ew':            op = DLFilterOp.EW
        elif op == 'not_ew':        op = DLFilterOp.NOT_EW
        elif op == 'contains':      op = DLFilterOp.CONTAINS
        elif op == 'not_contains':  op = DLFilterOp.NOT_CONTAINS
        elif op == 'sw':            op = DLFilterOp.SW
        elif op == 'not_sw':        op = DLFilterOp.NOT_SW
    if 'right' in value:
        right = value['right']

    return DLFilter(left, op, right)

def convert_sort(value):
    newstr = ''

    if is_boolean(value):
        newstr = str(value).lower()
    elif is_number(value) or is_string(value):
        newstr = str(value)
    else:
        for i in range(0, len(value)):
            if is_boolean(value[i]):
                newstr = newstr + str(value[i]).lower()
            elif is_number(value[i]) or is_string(value[i]):
                newstr = newstr + str(value[i])
            else:
                if 'field' in value[i]:
                    if 'field' in value[i]:
                        newstr = newstr + str(value[i]['field'])
                    if 'type' in value[i]:
                        newstr = newstr + ':' + str(value[i]['type'])
                else:
                    newstr = newstr + str(value[i])

            if i < len(value) - 1:
                newstr = newstr + ','
    
    return newstr

def handle_test(data, test):
    result = 'FAIL'

    if data == test['expected']['data']:
        result = 'PASS'

    print json.dumps({
        'name': test['name'],
        'expected': test['expected'],
        'actual': {
            'statusCode': 200,
            'exception': '',
            'data': data,
        },
        'result': result,
    })

    if result == 'PASS':
        return True
    return False

def handle_exception(e, test):
    result = 'FAIL'

    if (e.status_code == test['expected']['statusCode']
        and e.response['message'] == test['expected']['data']
        and e.response['code'] == test['expected']['exception']):
        result = 'PASS'

    print json.dumps({
        'name': test['name'],
        'expected': test['expected'],
        'actual': {
            'statusCode': e.status_code,
            'exception': e.response['code'],
            'data': e.response['message'],
        },
        'result': result,
    })

    if result == 'PASS':
        return True
    return False

def get_list(connection, test):
    success = False
    try:
        connection.authenticate(test['parameters']['key'], test['parameters']['secret'])
        data = connection.get_list()
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def get_schema(connection, test):
    success = False
    try:
        connection.authenticate(test['parameters']['key'], test['parameters']['secret'])
        data = connection.get_schema(test['dataset'])
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def read(connection, test):
    success = False
    try:
        connection.authenticate(test['parameters']['key'], test['parameters']['secret'])

        params = DLReadParams()
        if 'fields' in test['parameters']:
            params.fields = test['parameters']['fields']
        if 'filter' in test['parameters']:
            params.filter = convert_filter(test['parameters']['filter'])
        if 'limit' in test['parameters']:
            params.limit = test['parameters']['limit']
        if 'skip' in test['parameters']:
            params.skip = test['parameters']['skip']
        if 'sort' in test['parameters']:
            params.sort = convert_sort(test['parameters']['sort'])
        if 'total' in test['parameters']:
            params.total = test['parameters']['total']

        data = connection.read(test['dataset'], params)
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

if len(sys.argv) < 3 or len(sys.argv) > 5:
    print 'ERROR: invalid format: python test.py <apikey> <testdir> [ <host> <port> ]'
    sys.exit(1)

num_passed = 0
total_tests = 0
valid_key = sys.argv[1]
dirname = sys.argv[2]

host = None
if len(sys.argv) >= 4:
    host = sys.argv[3]

port = None
if len(sys.argv) >= 5:
    port = sys.argv[4]

connection = DLConnection(host = host, port = port)

files = os.listdir(dirname)
for filename in sorted(files):
    if filename.endswith('.json') == True:

        jsondata = json.load(open(dirname + '/' + filename))
        num_tests = len(jsondata['tests'])
        total_tests = total_tests + num_tests

        for i in range(0, num_tests):
            test = jsondata['tests'][i]

            # skip test if python listed
            if 'skip_languages' in test and 'python' in test['skip_languages']:
                total_tests = total_tests - 1
                continue

            if test['parameters']['key'] == 'valid_key':
                test['parameters']['key'] = valid_key;

            success = False

            if test['method'] == 'list':
                success = get_list(connection, test)
            elif test['method'] == 'schema':
                success = get_schema(connection, test)
            elif test['method'] == 'read':
                success = read(connection, test)
            else:
                print 'ERROR: ' + test['method'] + ' method not found'

            if success == True:
                num_passed = num_passed + 1

print '-------------------------------'
print 'passed: ' + str(num_passed)
print 'failed: ' + str(total_tests - num_passed)
print 'total:  ' + str(total_tests)
