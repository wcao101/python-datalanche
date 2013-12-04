#! /usr/bin/python
#
# Show the given table's details. Must have read access for the given database.
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery('my_database')
    q.describe_table('my_schema.my_table')

    result = client.query(q)

    print json.dumps(result)

except DLException as e:
    print repr(e)
