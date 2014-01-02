#! /usr/bin/python
#
# Update rows in the given table. Must have write access for the given database.
#
# equivalent SQL:
# UPDATE my_schema.my_table SET col3 = 'hello world' WHERE col3 = 'hello';
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery('my_database')
    q.update('my_schema.my_table')
    q.set({
        'col3': 'hello world'
    })
    q.where(q.expr(q.column('col3'), '=', 'hello'))

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
