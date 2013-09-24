#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient()
    client.key('your_API_key')
    client.secret('your_API_secret')

    e = DLExpression()
    e.column('col3').equals('hello')

    # q.where() is optional however all rows will be deleted
    # from the table if missing.
    q = DLQuery()
    q.delete_from('my_table')
    q.where(e)

    result = client.query(q)
    # if request or response is needed:
    # print json.dumps(result['request']), "\n"
    # print json.dumps(result['response']), "\n"
    print "row has been deleted successfully!!\n"
except DLException as e:
    print repr(e)
