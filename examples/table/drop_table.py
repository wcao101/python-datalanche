#! /usr/bin/python
#
# Drop the given table. Must have admin access for the given database.
#
# equivalent SQL:
# DROP TABLE my_schema.my_table CASCADE;
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery(database='my_database')
    q.drop_table('my_schema.my_table')
    q.cascade(True)

    client.query(q)

    print "drop_table succeeded!\n"

except DLException as e:
    print repr(e)
