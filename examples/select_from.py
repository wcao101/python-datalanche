#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery()
    q.select([ 'col1', 'col2' ])
    q.from_tables('my_table')
    q.where(q.expr(q.column('col3'), '$like', '%hello%'))
    q.order_by([
        q.expr(q.column('col1'), '$asc'),
        q.expr(q.column('col2'), '$desc')
    ])
    q.offset(0)
    q.limit(10)
    q.total(True)
    
    result = client.query(q)
    json.dumps(result['data'])

except DLException as e:
    print repr(e)
