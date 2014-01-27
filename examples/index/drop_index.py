#! /usr/bin/python
#
# Drop the given index. Must have admin access for the given database.
#
# equivalent SQL:
# DROP INDEX my_schema.my_index CASCADE;
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery(database='my_database')
    q.create_index('my_index')
    q.cascade(True)

    client.query(q)

    print "drop_index succeeded!\n"

except DLException as e:
    print repr(e)
