#! /usr/bin/python
#
# Alter the given database's properties. Must have admin access for the database.
#
# equivalent SQL:
# ALTER DATABASE my_database RENAME TO my_new_database;
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery()
    q.alter_database('my_database')
    q.rename_to('my_new_database')
    q.description('my_new_database description text')

    client.query(q)

    print "alter_database succeeded!\n"

except DLException as e:
    print repr(e)
