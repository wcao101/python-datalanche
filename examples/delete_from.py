#! /usr/bin/python

import json
from datalanche import *

try:
    
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    # q.where() is optional however all rows will be deleted
    # from the table if missing.

    e = DLExpression()
    e.column('col3').equals('hello')

    q = DLQuery()
    q.delete_from('my_table')
    q.where(e)

    data = client.query(q)
    print "row has been successfully deleted!\n"
except DLException as e:
    print repr(e)
