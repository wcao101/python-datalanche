#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')

    q = DLQuery()
    q.get_table_info('my_table')
    
    result = client.query(q)
    # if request or response is needed:
    # print json.dumps(result['request']), "\n"
    # print json.dumps(result['response']), "\n"
    print "The info of the table: ", json.dumps(result['data'])
except DLException as e:
    print repr(e)
