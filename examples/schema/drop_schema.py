#! /usr/bin/python
#
# Drop the given schema. Must have admin access for the given database.
#
# equivalent SQL:
# DROP SCHEMA my_schema CASCADE;
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery('my_database')
    q.drop_schema('my_schema')
    q.cascade(True)

    client.query(q)

    print "drop_schema succeeded!\n"

except DLException as e:
    print repr(e)
