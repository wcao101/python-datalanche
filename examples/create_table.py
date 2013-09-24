#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret') 

    # Only q.createTable() is required. The rest are optional
    # and the server will set defaults.
    q = DLQuery()
    q.create_table('my_9_table')
    q.description('my_table description text')
    q.is_private(True)
    q.license({
        'name' : 'license name',
        'url' : 'http://license.com',
        'description' : 'license description text'
    })
    q.sources([
        {
            'name' : 'source1',
            'url' : 'http://source1.com',
            'description' : 'source1 description text'
        },
        {
            'name' : 'source2',
            'url' : 'http://datalanche.com',
            'description' : 'source2 description text'
        },
    ])
    q.columns([
        {
            'name' : 'col1',
            'data_type' : 'uuid',
            'description' : 'col1 description text'
        },
        {
            'name' : 'col2',
            'data_type' : 'timestamp',
            'description' : 'col2 description text'
        },
        {
            'name' : 'col3',
            'data_type' : 'string',
            'description' : 'col3 description text'
        }
    ])
    
    data = client.query(q)
    print "table has been succefully created!\n",data
except DLException as e:
    print "the debug info is: "
    print repr(e)
    
