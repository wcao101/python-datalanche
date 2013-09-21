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
    
    q.update('my_n_table')
    q.set({
        'col3' : 'hello world'
    })
    q.where(e)
    
    
    client.query(q)
    print "The table has been succefully updated! "
        
except DLException as e:
    print repr(e)
