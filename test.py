# -*- coding: utf-8 -*-

from datalanche import *
import collections
import decimal
import csv
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

def convert_simple_filter(filter):

    if isinstance(filter, dict) == False:
        return filter

    has_not = False

    keys = filter.keys()
    column = keys[0]
    op_expr = filter[column]

    keys = op_expr.keys()
    operator = keys[0]
    value = op_expr[operator]

    if operator == '$not':
        has_not = True
        keys = value.keys()
        operator = keys[0]
        value = value[operator]

    new_filter = DLFilter()

    if operator == '$ends':
        if has_not == False:
            new_filter.column(column).ends_with(value)
        else:
            new_filter.column(column).not_ends_with(value)
    elif operator == '$contains':
        if has_not == False:
            new_filter.column(column).contains(value)
        else:
            new_filter.column(column).not_contains(value)
    elif operator == '$eq':
        if has_not == False:
            new_filter.column(column).equals(value)
        else:
            new_filter.column(column).not_equals(value)
    elif operator == '$gt':
        if has_not == False:
            new_filter.column(column).greater_than(value)
        else:
            new_filter.column(column).less_than_equal(value)
    elif operator == '$gte':
        if has_not == False:
            new_filter.column(column).greater_than_equal(value)
        else:
            new_filter.column(column).less_than(value)
    elif operator == '$in':
        if has_not == False:
            new_filter.column(column).any_in(value)
        else:
            new_filter.column(column).not_any_in(value)
    elif operator == '$lt':
        if has_not == False:
            new_filter.column(column).less_than(value)
        else:
            new_filter.column(column).greater_than_equal(value)
    elif operator == '$lte':
        if has_not == False:
            new_filter.column(column).less_than_equal(value)
        else:
            new_filter.column(column).greater_than(value)
    elif operator == '$starts':
        if has_not == False:
            new_filter.column(column).starts_with(value)
        else:
            new_filter.column(column).not_starts_with(value)

    return new_filter

def convert_filter(filter):

    if isinstance(filter, dict) == False:
        return filter

    keys = filter.keys()
    operator = keys[0]

    if operator == '$and' or operator == '$or':
        filter_list = filter[operator]

        new_filter_list = list()
        for f in filter_list:
            new_filter_list.append(convert_filter(f))

        if operator == '$and':
            return DLFilter().bool_and(new_filter_list)
        else:
            return DLFilter().bool_or(new_filter_list)
    else:
        return convert_simple_filter(filter)

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
                newstr = newstr + str(value[i])

            if i < len(value) - 1:
                newstr = newstr + ','
    
    return newstr

def get_records_from_file(filename):
    records = list()

    infile = open(filename, 'rb')
    reader = csv.reader(infile, delimiter=',', quotechar='\"', escapechar='\\')

    for i, row in enumerate(reader):
        if i != 0:
            records.append({
                'record_id': row[0],
                'name': row[1],
                'email': row[2],
                'address': row[3],
                'city': row[4],
                'state': row[5],
                'zip_code': row[6],
                'phone_number': row[7],
                'date_field': row[8],
                'time_field': row[9],
                'timestamp_field': row[10],
                'boolean_field': row[11],
                'int16_field': row[12],
                'int32_field': row[13],
                'int64_field': row[14],
                'float_field': row[15],
                'double_field': row[16],
                'decimal_field': row[17]
            })

    return records

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

def add_columns(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.add_columns(test['parameters']['dataset'], test['body']['columns'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def create_dataset(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.create_dataset(test['body'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def delete_dataset(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.delete_dataset(test['parameters']['dataset'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def delete_records(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.delete_records(test['parameters']['dataset'], convert_filter(test['parameters']['filter']))
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def get_dataset_list(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        data = client.get_dataset_list()

        # getDatasetList() test is a bit different than the rest
        # because a server can have any number of datasets. We test
        # that the expected dataset(s) is listed rather than
        # checking the entire result is valid, but only if a valid
        # response is expected.

        datasets = list()
        
        for i in range(0, data['num_datasets']):
            dataset = data['datasets'][i]

            # too variable to test
            try:
                del dataset['last_updated']
            except Exception as e:
                # ignore error
                print repr(e)
            try:
                del dataset['when_created']
            except Exception as e:
                # ignore error
                print repr(e)

            for j in range(0, test['expected']['data']['num_datasets']):
                if dataset == test['expected']['data']['datasets'][j]:
                    datasets.append(dataset)
                    break

        data = collections.OrderedDict()
        data['num_datasets'] = len(datasets)
        data['datasets'] = datasets

        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def get_schema(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        data = client.get_schema(test['parameters']['dataset'])

        # Delete date/time properties since they are probably
        # different than the test data. This is okay because
        # the server sets these values on write operations.
        del data['when_created']
        del data['last_updated']

        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def insert_records(client, test, filename):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        if test['body'] == 'dataset_file':
            records = get_records_from_file(filename)
            client.insert_records(test['parameters']['dataset'], records)
        else:
            client.insert_records(test['parameters']['dataset'], test['body']['records'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def read_records(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']

        params = DLReadParams()
        if 'columns' in test['parameters']:
            params.columns = test['parameters']['columns']
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

        data = client.read_records(test['parameters']['dataset'], params)
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def remove_columns(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.remove_columns(test['parameters']['dataset'], test['parameters']['columns'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def set_details(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.set_details(test['parameters']['dataset'], test['body'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def update_columns(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.update_columns(test['parameters']['dataset'], test['body'])
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def update_records(client, test):
    success = False
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        client.update_records(test['parameters']['dataset'], test['body'], convert_filter(test['parameters']['filter']))
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

if len(sys.argv) < 4 or len(sys.argv) > 7:
    print 'ERROR: invalid format: python test.py <apikey> <apisecret> <testfile> [ <host> <port> <verify_ssl> ]'
    sys.exit(1)

num_passed = 0
total_tests = 0
valid_key = sys.argv[1]
valid_secret = sys.argv[2]
test_file = sys.argv[3]

host = None
if len(sys.argv) >= 5:
    host = sys.argv[4]

port = None
if len(sys.argv) >= 6:
    port = sys.argv[5]

verify_ssl = True
if len(sys.argv) >= 7:
    verify_ssl = sys.argv[6].lower()
    if verify_ssl == '0' or verify_ssl == 'false':
        verify_ssl = False
    else:
        verify_ssl = True

client = DLClient(key = valid_key, secret = valid_secret, host = host, port = port, verify_ssl = verify_ssl)

try:
    client.delete_dataset('test_dataset')
except Exception as e:
    print repr(e)
    # ignore error

try:
    client.delete_dataset('new_test_dataset')
except Exception as e:
    print repr(e)
    # ignore error

test_suites = json.load(open(test_file), object_pairs_hook=collections.OrderedDict)
root_dir = os.path.dirname(test_file)
dataset_file = root_dir + '/' + test_suites['dataset_file']
files = test_suites['suites']['all']

for filename in files:

    jsondata = json.load(open(root_dir + '/' + filename), object_pairs_hook=collections.OrderedDict)
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
        if test['parameters']['secret'] == 'valid_secret':
            test['parameters']['secret'] = valid_secret;

        success = False

        if test['method'] == 'add_columns':
            success = add_columns(client, test)
        elif test['method'] == 'create_dataset':
            success = create_dataset(client, test)
        elif test['method'] == 'delete_dataset':
            success = delete_dataset(client, test)
        elif test['method'] == 'delete_records':
            success = delete_records(client, test)
        elif test['method'] == 'insert_records':
            success = insert_records(client, test, dataset_file)
        elif test['method'] == 'get_dataset_list':
            success = get_dataset_list(client, test)
        elif test['method'] == 'get_schema':
            success = get_schema(client, test)
        elif test['method'] == 'read_records':
            success = read_records(client, test)
        elif test['method'] == 'remove_columns':
            success = remove_columns(client, test)
        elif test['method'] == 'set_details':
            success = set_details(client, test)
        elif test['method'] == 'update_columns':
            success = update_columns(client, test)
        elif test['method'] == 'update_records':
            success = update_records(client, test)
        else:
            print 'ERROR: ' + test['method'] + ' method not found'

        if success == True:
            num_passed = num_passed + 1

print '-------------------------------'
print 'passed: ' + str(num_passed)
print 'failed: ' + str(total_tests - num_passed)
print 'total:  ' + str(total_tests)
