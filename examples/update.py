#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    q = DLQuery()
    
    e = DLExpression()
    e.column('col3').contains('hello')
    
    q.update('my_table')
    q.set({
        'col3' : 'hello world'
    })
    q.where(e)
    
    
    client.query(q)
    print "The table has been succefully updated! "
        
except DLException as e:
    print repr(e)
