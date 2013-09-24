#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(host='localhost', port=4001, verify_ssl=False)
    client.key('7zNN1Pl9SQ6lNZwYe9mtQw==')
    client.secret('VCBA1hLyS2mYdrL6kO/iKQ==')

    e = DLExpression()
    e.column('col3').equals('hello')

    # q.where() is optional however all rows will be deleted
    # from the table if missing.
    q = DLQuery()
    q.delete_from('my_table')
    q.where(e)

    data = client.query(q)
    if 200 <= data['response']['http_status'] < 300:
        print "row has been successfully deleted!\n"
except DLException as e:
    print repr(e)
