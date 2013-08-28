# -*- coding: utf-8 -*-

from datalanche import *
from requests.auth import HTTPBasicAuth
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
    print "Testing handle_test( ", test['name']," ) ..."
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
    message =  e.response['message']
    
    
    ## Postgres errors sometimes start with "Error:" or "error:". Not sure why.
    ## We should be case-insenitive in this case, and match the definition in
    ## the tests.

    if (message[0] == 'e' 
        and message[1] == 'r' 
        and message[2] == 'r'):
        message =  message.replace(message[0],'E',1)
                
        if (e.status_code == test['expected']['statusCode']
            and message == test['expected']['data']
            and e.response['code'] == test['expected']['exception']):
            result = 'PASS'
            
        print "\n"
        print "Testing handle_exception( ", test['name']," ) ..."
        print json.dumps({
            'name': test['name'],
            'expected': test['expected'],
            'actual': {
                  'statusCode': e.status_code,
                'exception': e.response['code'],
                'data': message,
            },
            'result': result,
        })
        print "\n"
            
    else:
        if (e.status_code == test['expected']['statusCode']
            and e.response['message'] == test['expected']['data']
            and e.response['code'] == test['expected']['exception']):
            result = 'PASS'
            
    
        print "\n"
        print "Testing handle_exception( ", test['name']," ) ..."
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
    
def use_raw_query(keys,params):
    use_raw = False
    for k in params.keys():
        if(k not in keys):
            use_raw = True
    
    return use_raw

# For testing unkown parameters. The API prevents users from adding
# unknown parameters so we need to circumvent it.
def query_raw(url_type,base_url,body):

    client.client.auth = HTTPBasicAuth(client.auth_key, client.auth_secret)
    url = client.url + base_url

    if (url_type == 'del'):
        r = client.client.delete (
            url,
            headers ={'Content-type':'application/json'},
            verify = client.verify_ssl    
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json(object_pairs_hook=collections.OrderedDict)

    if (url_type == 'post'):
        r = client.client.post ( 
            url,
            headers ={'Content-type':'application/json'},
            data = json.dumps(body),
            verify = client.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json(object_pairs_hook=collections.OrderedDict)
                
    if (url_type == 'get'):
        r = client.client.get (
            url,
            headers ={'Content-type':'application/json'},
            verify = client.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json(object_pairs_hook=collections.OrderedDict)

def alter_table(test):

    success = False
    q = DLQuery()
    keys = [
        'name',
        'rename',
        'description',
        'is_private',
        'license',
        'sources',
        'add_columns',
        'drop_columns',
        'alter_columns',
    ]

    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        
        ## Delete key and secret from params. They can screw up
        ## raw query test and client's auth has already been set to them.
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys,test['parameters'])
        if(use_raw == True):
                query_raw('post','/alter_table',test['parameters'])
        
        else:
            if ('name' in test['parameters']
                and test['parameters']['name'] != 'null'
                and test['parameters']['name'] != ''):
                q.alter_table(test['parameters']['name'])
            else:
                q.alter_table(None)
            if('rename' in test['parameters']):
                q.rename(test['parameters']['rename'])
            if('description' in test['parameters']):
                q.description(test['parameters']['description'])
            if('is_private' in test['parameters']):
                q.is_private(test['parameters']['is_private'])
            if('license' in test['parameters']):
                q.license(test['parameters']['license'])
            if('sources' in test['parameters']):
                q.sources(test['parameters']['sources'])
            if('add_columns' in test['parameters']):
                if(isinstance(test['parameters']['add_columns'],list)):
                    for i in test['parameters']['add_columns']:
                        q.add_column(i)
                    else:
                        q.params['add_columns'] = test['parameters']['add_columns']
            if('drop_columns' in test['parameters']):
                if(isinstance(test['parameters']['drop_columns'],list)):
                    for i in test['parameters']['drop_columns']:
                        q.drop_column(i)
                else:
                    q.params['drop_columns'] = test['parameters']['drop_columns']
            if('alter_columns' in test['parameters']):
                if(isinstance(test['parameters']['alter_columns'],dict) and 
                   len(test['parameters']['alter_columns'].keys()) > 0):
                    
                    for key, value in test['parameters']['alter_columns'].items():
                        q.alter_column(key, value)
                else:
                    q.params['alter_columns'] = test['parameters']['alter_columns']


        data = client.query(q)
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
    return success

def create_table(test):

    keys = [
        'name',
        'description',
        'is_private',
        'license',
        'sources',
        'columns',
    ]
    
    success = False
    q = DLQuery()
    data = None
    
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']

        use_raw = use_raw_query(keys,test['parameters'])
        if (use_raw == True):
            data = query_raw('post','/create_table',test['parameters'])
                            
        else:
             
            if('name' in test['parameters'] 
               and test['parameters']['name'] != 'null'
               and test['parameters']['name'] != ''):
                q.create_table(test['parameters']['name'])
            else:
                q.create_table(None)
            if('description' in test['parameters']):
                q.description(test['parameters']['description'])
            if('is_private' in test['parameters']):
                q.is_private(test['parameters']['is_private'])
            if('license' in test['parameters']):
                q.license(test['parameters']['license'])
            if('sources' in test['parameters']):
                q.sources(test['parameters']['sources'])
            if('columns' in test['parameters']):
                q.columns(test['parameters']['columns'])
                
            data = client.query(q)

        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
    return success

def drop_table(test):
    success = False
    q = DLQuery()
    keys = ['name']
    data = None
        
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys,test['parameters'])
        if (use_raw == True):
            data = query_raw('del','/drop_table',test['parameters'])
        
        else:
            if ('name' in test['parameters']
                and  test['parameters']['name'] != 'null'
                and test['parameters']['name'] != ''):
                q.drop_table(test['parameters']['name'])
            else:
                q.drop_table(None)
            
            data = client.query(q)
                
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
    return success
    
def delete_from(test):
    success = False
    q = DLQuery()
        
    keys = ['name','where']
    data = None
    
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys,test['parameters'])
        if (use_raw == True):
            data = query_raw('post','/delete_from',test['parameters'])
        
        else:
            if ('name' in test['parameters']
                and test['parameters']['name'] != 'null'
                and test['parameters']['name'] != ''):
                q.delete_from(test['parameters']['name'])
            else:
                q.delete_from(None)
            
            if('where' in test['parameters']):
                q.where(test['parameters']['where'])
           
            data = client.query(q)
            
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
    return success

def get_table_list(test):
    success = False
    q = DLQuery()
    keys = list()
    
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        tables = list()
                
        use_raw = use_raw_query(keys,test['parameters'])
        if (use_raw == True):
            print "The params is using raw_query..\n"
            print "and the data is: ", data, "\n"
                    
            if (test['expected']['statusCode'] == 200):
                data = query_raw('get','/get_table_list',test['parameters'])
                               
                for i in range(0, data['num_tables']):
                    table = data['tables'][i]
                    
                    try:
                        del table['last_updated']
                    except Exception as e:
                        # ignore error
                        #print repr(e)
                        pass
                        
                    try:
                        del table['when_created']
                    except Exception as e:
                        # ignore error
                        #print repr(e)
                        pass
                    
                    for j in range(0, test['expected']['data']['num_tables']):
                        if table == test['expected']['data']['tables'][j]:
                            tables.append(table)
                            break
        
        # getDatasetList() test is a bit different than the rest
        # because a server can have any number of datasets. We test
        # that the expected dataset(s) is listed rather than
        # checking the entire result is valid, but only if a valid
        # response is expected.
        else:
            if (test['expected']['statusCode'] == 200):
                q.get_table_list()
                data = client.query(q)

                print "The params is using default query..\n"
                print "and the data is: ", data


                for i in range(0, data['num_tables']):
                    table = data['tables'][i]
                    
                    # too variable to test
                    try:
                        del table['last_updated']
                    except Exception as e:
                        # ignore error
                        #print repr(e)
                        pass
                        
                    try:
                        del table['when_created']
                    except Exception as e:
                        # ignore error
                        #print repr(e)
                        pass
                        
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
        # print repr(e)
        pass
    return success

def get_table_info(test):
    success = False
    q = DLQuery()
    keys = ['name']
    data = None

    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys,test['parameters'])
        if (use_raw == True):
           data =  query_raw('get','/get_table_info',test['parameters'])

           # Delete date/time properties since they are probably
           # different than the test data. This is okay because
           # the server sets these values on write operations.
           del data['when_created']
           del data['last_updated']

           success = handle_test(data, test)
                      
        else:
            if ('name' in test['parameters']
                and test['parameters']['name'] != 'null'
                and test['parameters']['name'] != ''):
                q.get_table_info(test['parameters']['name'])
            else:
                q.get_table_info(None)

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
        #print repr(e)
        pass
    return success

def insert_into(test):
    success = False
    q = DLQuery()

    keys = ['name','values']
    data = None

    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys, test['parameters'])
        if (use_raw == True):
            data = query_raw('post', '/insert_into', test['parameters'])
            
        else:
            if ('name' in test['parameters']
                and test['parameters']['name'] != 'null'
                and test['parameters']['name'] != ''):
                q.insert_into(test['parameters']['name'])
            else:
                q.insert_into(None)
                
            if test['parameters']['values'] == 'dataset_file':
                records = get_records_from_file(filename)
                q.values(records)
                data = client.quer(q)
            else:
                q.values(test['parameters']['values'])
                data = client.query(q)

        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
    return success

def select_from(test):
    
    success = False
    q = DLQuery()
#    q.debug(True)
    
    keys = [
        'select',
        'distinct',
        'from',
        'where',
        'group_by',
        'order_by',
        'offset',
        'limit',
        'total'
    ]
    data = None

    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys,test['parameters'])
        if (use_raw == True):
            data = query_raw('post', '/select_from',test['parameters'])
                        
        else:
            if('from' in test['parameters']
               and test['parameters']['from'] != 'null'
               and test['parameters']['from'] != ''):
                q.from_table(test['parameters']['from'])
            else:
                q.from_table(None)
            
            if ('select' in test['parameters']):
                q.select(test['parameters']['select'])
            if ('distinct' in test['parameters']):
                q.distinct(test['parameters']['distinct'])
            if('where' in test['parameters']):
                q.where(test['parameters']['where'])
            if('group_by' in test['parameters']):
                q.group_by(test['parameters']['group_by'])
            if('order_by' in test['parameters']):
                q.order_by(test['parameters']['order_by'])
            if('offset' in test['parameters']):
                q.offset(test['parameters']['offset'])
            if('limit' in test['parameters']):
                q.limit(test['parameters']['limit'])
            if('total' in test['parameters']):
                q.total(test['parameters']['total'])
            
            data = client.query(q)
            
        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
    return success
    
def update(test):
    success = False
    q = DLQuery()
    
    keys = ['name','set','where']
    data = None
    
    try:
        client.auth_key = test['parameters']['key']
        client.auth_secret = test['parameters']['secret']
        del test['parameters']['key']
        del test['parameters']['secret']
        
        use_raw = use_raw_query(keys, test['parameters'])
        if(use_raw == True):
            data = query_raw('post', '/update', test['parameters'])
            
        else:

            if ('name' in test['parameters']
                and test['parameters']['name']
                and test['parameters']['name']):
                q.update(test['parameters']['name'])
            else:
                q.update(None)

            if('set' in test['parameters']):
                q.set(test['parameters']['set'])
            if('where' in test['parameters']):
                q.where(test['parameters']['where'])

            data = client.query(q)

        success = handle_test(data, test)
    except DLException as e:
        success = handle_exception(e, test)
    except Exception as e:
        #print repr(e)
        pass
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
