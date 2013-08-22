# -*- coding: utf-8 -*-

from datalanche import *
import collections
import decimal
import csv
import json
import os
import sys


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
    
    print "\n"
    print "testing handle_test()...", test['name']
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

    print "\n"
    if result == 'PASS':
        return True
    return False

def handle_exception(e, test):
    result = 'FAIL'

    if (e.status_code == test['expected']['statusCode']
        and e.response['message'] == test['expected']['data']
        and e.response['code'] == test['expected']['exception']):
        result = 'PASS'
    
    print "\n"
    print "Testing handle_exception()...", test['name']
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
    print "\n"
    
    if result == 'PASS':
        return True
    return False

def alter_table(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        
        for key, value in test['parameters'].items():
            if (key == 'name'):
                q.alter_table(value)
            elif(key == 'rename'):
                q.rename(value)
            elif(key == 'description'):
                q.description(value)
            elif(key == 'is_private'):
                q.is_private(value)
            elif(key == 'license'):
                q.license(value)
            elif(key == 'sources'):
                q.sources(value)
            elif(key == 'add_columns'):
                if(isinstance(test['parameters']['add_columns'],list)):
                    for i in test['parameters']['add_columns']:
                        q.add_column(i)
                else:
                    q.params['add_columns'] = test['parameters']['add_columns']
            elif(key == 'drop_columns'):
                if(isinstance(test['parameters']['drop_columns'],list)):
                    for i in test['parameters']['drop_columns']:
                        q.drop_column(i)
                else:
                    q.params['drop_columns'] = test['parameters']['drop_columns']
            elif(key == 'alter_columns'):
                if(isinstance(test['parameters']['alter_columns'],dict) and 
                   len(test['parameters']['alter_columns'].keys()) > 0):

                    for key, value in test['parameters']['alter_columns'].items():
                        q.alter_column(key, value)
                else:
                    q.params['alter_columns'] = test['parameters']['alter_columns']


        client.query(q)
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def create_table(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']

        if ('name' not in test['parameters'].keys()):
            q.create_table(None)
        
        for key,value in test['parameters'].items():
            if(key == 'name'):
                q.create_table(value)
            elif(key == 'description'):
                q.description(value)
            elif(key == 'is_private'):
                q.is_private(value)
            elif(key == 'license'):
                q.license(value)
            elif(key == 'sources'):
                q.sources(value)
            elif(key == 'columns'):
                q.columns(value)
            else:
                q.unknown(value)
                
        client.query(q)
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def drop_table(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']

        if ('name' not in test['parameters'].keys()):
            q.drop_table(None)

        q.drop_table(test['parameters']['name'])
        
        client.query(q)
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def delete_from(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        
        if ('name' not in test['parameters'].keys()):
            q.delete_from(None)
            
        for key,value in test['parameters'].items():
            if (key == 'name'):
                q.delete_from(value)
            elif(key == 'where'):
                q.where(value)

        client.query(q)
        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def get_table_list(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        q.get_table_list()
        data = client.query(q)

        # getDatasetList() test is a bit different than the rest
        # because a server can have any number of datasets. We test
        # that the expected dataset(s) is listed rather than
        # checking the entire result is valid, but only if a valid
        # response is expected.

        tables= list()
        
        for i in range(0, data['num_tables']):
            table = data['tables'][i]

            # too variable to test
            try:
                del table['last_updated']
            except Exception as e:
                # ignore error
                print repr(e)
            try:
                del table['when_created']
            except Exception as e:
                # ignore error
                print repr(e)

            for j in range(0, test['expected']['data']['num_tables']):
                if table == test['expected']['data']['tables'][j]:
                    tables.append(table)
                    break

        data = collections.OrderedDict()
        data['num_tables'] = len(tables)
        data['tables'] = tables

        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def get_table_info(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        
        if ('name' not in test['parameters'].keys()):
            q.get_table_info(None)

        q.get_table_info(test['parameters']['name'])
        data = client.query(q)

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

def insert_into(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        
        if ('name' not in test['parameters'].keys()):
            q.insert_into(None)
            
        q.insert_into(test['parameters']['name'])
        
        if test['parameters']['values'] == 'dataset_file':
            records = get_records_from_file(filename)
            q.values(records)
            client.quer(q)
        else:
            q.values(test['parameters']['values'])
            client.query(q)

        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def select_from(test):
    
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']

        if ('from_table' not in test['parameters'].keys()):
            q.from_table(None)
        
        for key, value in test['parameters'].items():
            if (key == 'select'):
                q.select(value)
            elif (key == 'distinct'):
                q.distinct(value)
            elif(key == 'from'):
                q.from_table(value)
            elif(key == 'where'):
                q.where(value)
            elif(key == 'group_by'):
                q.group_by(value)
            elif(key == 'order_by'):
                q.order_by(value)
            elif(key =='offset'):
                q.offset(value)
            elif(key == 'limit'):
                q.limit(value)
            elif(key == 'total'):
                q.total(value)

        data = client.query(q)
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

def update(test):
    success = False
    q = DLQuery()
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']

        for key, value in test['parameters'].items():
            if (key == 'name'):
                q.update(value)
            elif(key =='set'):
                q.set(value)
            elif(key=='where'):
                q.where(value)

        client.query(q)

        success = handle_test(None, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        print repr(e)
    return success

q = DLQuery()

try:
    client.query(q.drop_table('test_dataset'))
except Exception as e:
    # print repr(e)
    # ignore error

    try:
        client.query(q.drop_table('new_test_dataset'))
    except Exception as e:
        pass
        # print repr(e)
        # ignore error

# after the new_test_dataset is loaded...
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
        #### for debug....####
        #print test['parameters']['distinct']

        success = False

        if test['method'] == 'alter_table':
            success = alter_table(test)
        elif test['method'] == 'create_table':
            success = create_table(test)
        elif test['method'] == 'delete_from':
            success = delete_from(test)
        elif test['method'] == 'drop_table':
            success = drop_table(test)
        elif test['method'] == 'get_table_info':
            success = get_table_info(test)
        elif test['method'] == 'get_table_list':
            success = get_table_list(test)
        elif test['method'] == 'insert_into':
            success = insert_into(test)
        elif test['method'] == 'select_from':
            success = select_from(test)
        elif test['method'] == 'update':
            success = update(test)

        else:
            print 'ERROR: ' + test['method'] + ' method not found'

        if success == True:
            num_passed = num_passed + 1

print '-------------------------------'
print 'passed: ' + str(num_passed)
print 'failed: ' + str(total_tests - num_passed)
print 'total:  ' + str(total_tests)
