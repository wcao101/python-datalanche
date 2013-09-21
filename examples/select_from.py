#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(
        host = 'localhost', port = 4001, verify_ssl = False
    )
    client.key('7zNN1Pl9SQ6lNZwYe9mtQw==')
    client.secret('VCBA1hLyS2mYdrL6kO/iKQ==')


    q = DLQuery()
    
    e = DLExpression()
    e.column('col3').contains('hello')
    
    # if you want all columns use q.select('*')
    q.select([ 'col1', 'col2' ]) 
    q.from_table('my_table')
    q.where(e)
    q.order_by([
        { 'col1' : '$asc' },
        { 'col2' : '$desc' },
    ])
    q.offset(0)
    q.limit(1)
    q.total(False)
    
    
    data = client.query(q)
    print "The data is: ", json.dumps(data['data'])
        
except DLException as e:
    print repr(e)
