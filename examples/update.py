#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    e = DLExpression()
    e.column('col3').contains('hello')

    q = DLQuery()    
    q.update('my_table')
    q.set({
        'col3' : 'hello world'
    })
    q.where(e)
        
    result = client.query(q)
    # if request or response is needed:
    # print json.dumps(result['request']), "\n"
    # print json.dumps(result['response']), "\n"
    print "The table has been updated successfully!! "
except DLException as e:
    print repr(e)
