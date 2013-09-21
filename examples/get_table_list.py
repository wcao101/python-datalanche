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
    q.get_table_list()
    
    data = client.query(q)
    
    print "The list of the tables: ", data['data']
    
except DLException as e:
    print repr(e)
