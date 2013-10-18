#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    definition = {
        'schema_name': 'my_schema',
        'table_name': 'my_table',
        'description': 'my_table description text',
        'is_private': True,
        'license': {
            'name': 'public domain',
            'description': 'this table is public domain',
            'url': None
        },
        'sources': {
            'source1': {
                'url' : 'http://source1.com',
                'description' : 'source1 description text'
            },
            'source2': {
                'url' : 'http://source2.com',
                'description' : 'source2 description text'
            }
        },
        'columns': {
            'col1': {
                'data_type': 'uuid',
                'description': 'col1 description text',
                'not_null': True
            },
            'col2': {
                'data_type': 'text',
                'description': 'col2 description text',
                'default_value': None,
                'not_null': False
            },
            'col3': {
                'data_type': 'integer',
                'description': 'col3 description text',
                'default_value': 0,
                'not_null': True
            }
        },
        'constraints': {
            'primary_key': 'col1'
        },
        'indexes': {},
        'collaborators': {
            'bob': 'read',
            'slob': 'read/write',
            'knob': 'admin'
        }
    }

    q = DLQuery()
    q.create_table(definition)
    
    client.query(q)
    print 'create_table succeeded'

except DLException as e:
    print repr(e)
except Exception as ex:
    print repr(ex)
