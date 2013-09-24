#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    e = DLExpression()
    e.column('col3').contains('hello')
    
    # if you want all columns use q.select('*')
    q = DLQuery()
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
    if 200 <= data['response']['http_status'] < 300:    
        print "The data is: ", json.dumps(data['data'])
except DLException as e:
    print repr(e)
