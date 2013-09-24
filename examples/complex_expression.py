#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')
    
    e = DLExpression()
    e.bool_and([
        DLExpression().bool_or([
            DLExpression().column('col3').equals('hello'),
            DLExpression().column('col3').equals('world')
        ]),
        DLExpression().column('col1').equals(
            '0f21b968-cd28-4d8b-9ea6-33dbcd517ec5')
    ])

    q = DLQuery()    
    q.select('*').from_table('my_table').where(e)
    
    result = client.query(q)
    # if request or response is needed:
    # print json.dumps(result['request']), "\n"
    # print json.dumps(result['response']), "\n"
    print "the data is: ", json.dumps(result['data']),"\n"
except DLException as e:
    print repr(e)
