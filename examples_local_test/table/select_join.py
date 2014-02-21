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
    config = json.load(open("../config.json"))
    config['verify_ssl'] = config['verify_ssl'].lower()
    if config['verify_ssl'] == '0' or config['verify_ssl'] == 'false':
        config['verify_ssl'] = False
    else:
        config['verify_ssl'] = True

    client = DLClient(key = config['api_key'], 
                      secret = config['api_secret'], 
                      host = config['host'], 
                      port = config['port'], 
                      verify_ssl = config['verify_ssl'])

    q = DLQuery(database='my_database')
    q.select_all()
    q.from_tables(q.expr(
        q.table('my_schema.t1'),
        '$join', q.table('my_schema.t2'), '$on', q.column('my_schema.t1.col1'), '=', q.column('my_schema.t2.col1'),
        '$join', q.table('my_schema.t3'), '$on', q.column('my_schema.t1.col1'), '=', q.column('my_schema.t3.col1')
    ))

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
