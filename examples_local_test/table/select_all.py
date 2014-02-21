#! /usr/bin/python
#
# Select rows from the given table. Must have read access for the given database.
#
# equivalent SQL:
# SELECT DISTINCT col1, col2
#     FROM my_schema.my_table
#     WHERE col3 LIKE '%hello%'
#     ORDER BY col1 ASC, col2 DESC
#     OFFSET 0 LIMIT 10;
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
    q.distinct(True)
    q.from_tables('my_schema.my_table')
    q.where(q.expr(q.column('col3'), '$like', '%hello%'))
    q.order_by([
        q.expr(q.column('col1'), '$asc'),
        q.expr(q.column('col2'), '$desc')
    ])
    q.offset(0)
    q.limit(10)

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
