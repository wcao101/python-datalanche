#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')

    #  Only q.alterTable() is required. The rest are optional and, if present,
    #  will override current values. However add/drop/alter columns are broken
    #  up into individual functions and will do the appropriate function. Note
    #  that dropping or altering columns of an existing table can delete 
    #  existing data.
    q = DLQuery()
    q.alter_table('my_table')
    q.rename('my_new_table')
    q.description('my_new_table description text')
    q.is_private(False)
    q.license({
        'name' : 'new license name',
        'url' : 'http://new_license.com',
        'description' : 'new license description text'
    })
    q.sources([
        {
            'name' : 'new source1',
            'url' : 'http://new_source1.com',
            'description' : 'new source1 description text'
        },
        {
            'name' : 'new source2',
            'url' : 'http://new_source2.com',
            'description' : 'new source2 description text'
        },
    ])
    q.add_column({
        'name' : 'new_col',
        'data_type' : 'int32',
        'description' : 'new_col description text'
    })
    q.drop_column('col2')
    q.drop_column('col3')
    q.alter_column('col1', 
                  {
                      # will only alter col1's data type
                      'data_type' : 'string'
                  })
    
    client.query(q)
    if 200 <= data['response']['http_status'] < 300:
        print "Table has been successfully altered!\n"
except DLException as e:
    print repr(e)
