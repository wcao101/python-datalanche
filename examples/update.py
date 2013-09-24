#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    

    
    e = DLExpression()
    e.column('col3').contains('hello')

    q = DLQuery()    
    q.update('my_table')
    q.set({
        'col3' : 'hello world'
    })
    q.where(e)
        
    data = client.query(q)
    if 200 <= data['response']['http_status'] < 300:    
        print "The table has been succefully updated! "
except DLException as e:
    print repr(e)
