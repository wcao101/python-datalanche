#! /usr/bin/python
#
# Show the given schema's details. Must have read access for the given database.
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery(database='my_database')
    q.describe_schema('my_schema')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
