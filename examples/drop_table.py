#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(
        key='7zNN1Pl9SQ6lNZwYe9mtQw==', secret='VCBA1hLyS2mYdrL6kO/iKQ==', 
        host = 'localhost', port = 4001, verify_ssl = False
    )
    
    q = DLQuery()
    q.drop_table('test_dataset')
    
    data = client.query(q)
    
    print "table has been dropped/deleted\n", data
    
except DLException as e:
    print repr(e)
    
