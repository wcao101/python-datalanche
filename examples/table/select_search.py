#! /usr/bin/python
#
# Search the table and retrieve the rows. Must have read access for the given database.
#
# equivalent SQL:
# SELECT * FROM my_schema.my_table WHERE SEARCH 'hello world';
#
# NOTE: Search clause is sent to ElasticSearch. The search
# results are used as a filter when executing the SQL query.
#
import json
from datalanche import *

try:
    client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')

    q = DLQuery('my_database')
    q.select('*').from_tables('my_schema.my_table').search('hello world')

    result = client.query(q)

    print json.dumps(result)

except DLException as e:
    print repr(e)
