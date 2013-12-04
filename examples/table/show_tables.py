#! /usr/bin/python
#
# Show all tables you have access to.
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery()
    q.show_tables()

    result = client.query(q)

    print json.dumps(result)

except DLException as e:
    print repr(e)
