#! /usr/bin/python
#
# Insert rows into the given table. Must have write access for the given database.
#
# equivalent SQL:
# INSERT INTO my_schema.my_table (col1, col2, col3)
#     VALUES
#     ( '0f21b968-cd28-4d8b-9ea6-33dbcd517ec5', '2012-11-13T01:04:33.389Z', 'hello' ),
#     ( '8bf38716-95ef-4a58-9c1b-b7c0f3185746', '2012-07-26T01:09:04.140Z', 'world' ),
#     ( '45db0793-3c99-4e0d-b1d0-43ab875638d3', '2012-11-30T07:10:36.871Z', 'hello world' );
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
    q.insert_into('my_schema.my_table')
    q.values([
        {
            'col1': '0f21b968-cd28-4d8b-9ea6-33dbcd517ec5',
            'col2': '2012-11-13T01:04:33.389Z',
            'col3': 'Hello',
            'col4': 'Ohio'
        },
        {
            'col1': '8bf38716-95ef-4a58-9c1b-b7c0f3185746',
            'col2': '2012-07-26T01:09:04.140Z',
            'col3': 'World',
            'col4': 'California'
        },
        {
            'col1': '45db0793-3c99-4e0d-b1d0-43ab875638d3',
            'col2': '2012-11-30T07:10:36.871Z',
            'col3': 'Hello World',
            'col4': 'Colorado'
        }
    ])

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
