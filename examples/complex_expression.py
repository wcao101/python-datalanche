#! /usr/bin/python

import json
from datalanche import *

try:
    
    client = DLClient(
        key='7zNN1Pl9SQ6lNZwYe9mtQw==', secret='VCBA1hLyS2mYdrL6kO/iKQ==', 
        host = 'localhost', port = 4001, verify_ssl = False
    )
    
    e = DLExpression()
    
    q = DLQuery()
     
    e.bool_and([
        DLExpression().bool_or([
             DLExpression().column('col3').equals('hello'),
            DLExpression().column('col3').equals('world')
        ]),
        DLExpression().column('col1').equals('0f21b968-cd28-4d8b-9ea6-33dbcd517ec5')
    ])
    
    q.select('*').from_table('my_table').where(e)
    
    data = client.query(q)
    print "the data is: ", json.dumps(data)
except DLException as e:
    print repr(e)
