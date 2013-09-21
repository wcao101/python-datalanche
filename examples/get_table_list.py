#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    q = DLQuery()
    q.get_table_list()
    
    data = client.query(q)
    
    print "The list of the tables: ", json.dumps(data['data'])
    
except DLException as e:
    print repr(e)
