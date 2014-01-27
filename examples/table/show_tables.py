#! /usr/bin/python
#
# Show all tables you have access to.
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery(database='my_database')
    q.show_tables()

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
