#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')

    q = DLQuery()
    q.get_table_info('my_table')
    
    data = client.query(q)
    
    print "The info of the table: ", json.dumps(data['data'])
    
except DLException as e:
    print repr(e)
