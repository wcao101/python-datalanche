#! /usr/bin/python

import json
from datalanche import *

try:
    
    client = DLClient(
        key='7zNN1Pl9SQ6lNZwYe9mtQw==', secret='VCBA1hLyS2mYdrL6kO/iKQ==', 
        host = 'localhost', port = 4001, verify_ssl = False
    )
    
    # q.where() is optional however all rows will be deleted
    # from the table if missing.

    e = DLExpression()
    e.column('col3').equals('hello')

    q = DLQuery()
    q.delete_from('my_table')
    q.where(e)

    data = client.query(q)
    print "row has been successfully deleted!\n", data
except DLException as e:
    print repr(e)
