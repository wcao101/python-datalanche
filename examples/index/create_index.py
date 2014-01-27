#! /usr/bin/python
#
# Create an index on the given table. Must have admin access for the given database.
#
# equivalent SQL:
# CREATE UNIQUE INDEX my_index ON my_schema.my_table USING btree (col1, col2);
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery(database='my_database')
    q.create_index('my_index')
    q.unique(True)
    q.on_table('my_schema.my_table')
    q.method('btree')
    q.columns([ 'col1', 'col2' ])

    client.query(q)

    print "create_index succeeded!\n"

except DLException as e:
    print repr(e)
