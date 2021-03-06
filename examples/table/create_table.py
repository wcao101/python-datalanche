#! /usr/bin/python
#
# Create the given table. Must have admin access for the given database.
#
# equivalent SQL:
# CREATE TABLE my_schema.my_table(
#     col1 uuid NOT NULL,
#     col2 varchar(50),
#     col3 integer DEFAULT 0 NOT NULL
# );
#
import json
from datalanche import *
import sys, os

try:

    config = json.load(open(os.path.dirname(os.path.dirname(__file__))+'/config.json'))

    # Please find your API credentials here: https://www.datalanche.com/account before use            
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database') 
    q.create_table('my_schema.my_table')
    q.description('my_table optional description text')
    q.columns({
        'col1': {
            'data_type': {
                'name': 'uuid'
            },
            'description': 'col1 description text',
            'not_null': True
        },
        'col2': {
            'data_type': {
                'name': 'timestamptz'
            },
            'description': 'col2 description text',
            'default_value': None,
            'not_null': False
        },
        'col3': {
            'data_type': {
                'name': 'text'
            },
            'description': 'col3 description text',
            'default_value': 'default text',
            'not_null': True
        },
        'col4': {
            'data_type': {
                'name': 'varchar',
                'args': [ 50 ]
            },
            'description': 'col4 description text'
        },
    })

    client.query(q)

    print "create_table succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
