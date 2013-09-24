#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    q = DLQuery()
    q.insert_into('my_table')
    q.values([
        {
            'col1' : '0f21b968-cd28-4d8b-9ea6-33dbcd517ec5',
            'col2' : '2012-11-13T01:04:33.389Z',
            'col3' : 'hello'
        },
        {
            'col1' : '8bf38716-95ef-4a58-9c1b-b7c0f3185746',
            'col2' : '2012-07-26T01:09:04.140Z',
            'col3' : 'world'
        },
        {
            'col1' : '45db0793-3c99-4e0d-b1d0-43ab875638d3',
            'col2' : '2012-11-30T07:10:36.871Z',
            'col3' : 'hello world'
        }
    ])
    
    result = client.query(q)
    # if request or response is needed:
    # print json.dumps(result['request']), "\n"
    # print json.dumps(result['response']), "\n"
    print "rows inserted into my_table successfully!"
except DLException as e:
    print repr(e)
