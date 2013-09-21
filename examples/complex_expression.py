#! /usr/bin/python

import json
from datalanche import *

try:
    
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')

    
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
    print "the data is: ", json.dumps(data['data'])

except DLException as e:
    print repr(e)
