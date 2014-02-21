#! /usr/bin/python
#
# Alter the given table's properties. Must have admin access for the given database.
#
# equivalent SQL:
#
# BEGIN TRANSACTION;
#
# ALTER TABLE my_schema.my_table
#     DROP COLUMN col2,
#     ALTER COLUMN col1 DROP NOT NULL,
#     ALTER COLUMN col1 SET DATA TYPE text,
#     ADD COLUMN new_col integer;
# ALTER TABLE my_schema.my_table RENAME COLUMN col3 TO col_renamed;
# ALTER TABLE my_schema.my_table RENAME TO my_new_table;
# ALTER TABLE my_schema.my_new_table SET SCHEMA my_new_schema;
#
# COMMIT;
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
    q.alter_table('my_schema.my_table')
    q.set_schema('my_new_schema')
    q.rename_to('my_new_table')
    q.description('my_new_table description text')
    q.add_column('new_col', {
        'data_type': {
            'name': 'integer'
        },
        'description': 'new_col description text'
    })
    q.alter_column('col1', {
        'data_type': {
            'name': 'text'
        },
        'description': 'new col1 description text'
    })
    q.drop_column('col2')
    q.rename_column('col3', 'col_renamed')

    client.query(q)

    print "alter_table succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
