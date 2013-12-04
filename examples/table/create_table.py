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

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery('my_database')
    q.create_table('my_schema.my_table')
    q.description('my_table description text')
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
                'name': 'varchar',
                'args': [ 50 ]
            },
            'description': 'col2 description text',
            'default_value': None,
            'not_null': False
        },
        'col3': {
            'data_type': {
                'name': 'integer'
            },
            'description': 'col3 description text',
            'default_value': 0,
            'not_null': True
        }
    })

    client.query(q)

    print "create_table succeeded!\n"

except DLException as e:
    print repr(e)
