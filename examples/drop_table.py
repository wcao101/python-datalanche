#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    q = DLQuery()
    q.drop_table('my_table')
    
    data = client.query(q)
    
    print "table has been dropped/deleted\n"
    
except DLException as e:
    print repr(e)
    
