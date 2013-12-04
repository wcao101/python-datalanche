#! /usr/bin/python
#
# Show details of given database. Must have read access for the database.
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery()
    q.describe_database('my_database')

    result = client.query(q)

    print json.dumps(result)

except DLException as e:
    print repr(e)
