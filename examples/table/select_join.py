#! /usr/bin/python
#
# Join multiple tables and retrieve the rows. Must have read access for the given database.
#
# equivalent SQL:
# SELECT * FROM t1
#     JOIN t2 ON t1.c1 = t2.c1
#     JOIN t3 ON t1.c1 = t3.c1;
#
import json
from datalanche import *
import sys

try:

    config = json.load(open("../../config.json"))

    # Please found your API credentials here: datalanche.com/account/login before use
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.select_all()
    q.from_tables(q.expr(
        q.table('t1'),
        '$join', q.table('t2'), '$on', q.column('t1.c1'), '=', q.column('t2.c1'),
        '$join', q.table('t3'), '$on', q.column('t1.c1'), '=', q.column('t3.c1')
    ))

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
