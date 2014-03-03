API_CREDENTIALS =  GoyY7hI2S5igDS4pG2Vdyg==:e02C96sqR5mvUoQXkCC2Gg==
DB_QUERY_URL = https://api.datalanche.com/my_database/query 
QUERY_URL = https://api.datalanche.com/query 
CURL_OPTS_DROP_SCHEMA = -X POST -u "$(API_CREDENTIALS)" -H "Content-Type: application/json" -d '{ "drop_schema": "my_new_schema", "cascade": true }'
CURL_OPTS_ALTER_DATABASE = -X POST -u "$(API_CREDENTIALS)" -H "Content-Type: application/json" -d '{ "alter_database": "my_new_database", "rename_to": "my_database"}'

#host api.datalanche.com
all: target

target:  test

test: pre_test test_schema test_table test_selects test_index test_alter_schema test_database # run examples test
	
test_schema: pre_test
	# schema examples
	# create a schema
	python ./examples/schema/create_schema.py

	# describe the schema
	python ./examples/schema/describe_schema.py

	# show the created schema
	python ./examples/schema/show_schemas.py

test_table: test_schema
	# table examples
	# create a table
	python ./examples/table/create_table.py

	# describe the table
	python ./examples/table/describe_table.py

	# show the tables in my_database, should return 2 tables
	python ./examples/table/show_tables.py

	# insert data into my_schema.my_table
	python ./examples/table/insert.py

	# update my_schema.my_table
	python ./examples/table/update.py

	# delete my_schema.my_table
	python ./examples/table/delete.py

	# alther the table name and the table descriptions
	python ./examples/table/alter_table.py

	# create table again after altering table.
	python ./examples/table/create_table.py

	# show table to make sure the new table is created before drop
	python ./examples/table/show_tables.py

	# drop my_schema.my_table
	python ./examples/table/drop_table.py

	# show table to make sure the new table is created before drop
	python ./examples/table/show_tables.py

test_selects: test_schema
	# create sample tables for selects
	sh ./test/create_sample_tables

	# testing select example
	python ./examples/table/select_all.py

	# testing select_search example
	python ./examples/table/select_search.py

	# testing select_join example
	python ./examples/table/select_join.py

test_index: test_selects
	# create index on my_schema.my_table
	python ./examples/index/create_index.py

	# show the tables with index
	python ./examples/table/describe_table.py

	# drop index on my_schema.my_table
	python ./examples/index/drop_index.py

	# show the tables with dropped index
	python ./examples/table/describe_table.py

	# create index on my_schema.my_table again for testing alterring index
	python ./examples/index/create_index.py

	# show the tables with index
	python ./examples/table/describe_table.py

	# alter index on my_schema.my_table
	python ./examples/index/alter_index.py

	# show the tables with alterred index
	python ./examples/table/describe_table.py

test_alter_schema: test_schema
	#echo drop the schema: my_new_schema before testing alter_schema example
	curl $(DB_QUERY_URL) $(CURL_OPTS_DROP_SCHEMA)

	# alter my_schema to my_new_schema
	python ./examples/schema/alter_schema.py

	# show schema which should show my_new_schema
	python ./examples/schema/show_schemas.py

	#create the schema again to test drop schema.
	python ./examples/schema/create_schema.py

	# show schema which should show my_schema and my_new_schema
	python ./examples/schema/show_schemas.py

	# drop my_schema
	python ./examples/schema/drop_schema.py

	# show schema which should show new_schema only
	python ./examples/schema/show_schemas.py

test_database:
	# database examples
	# describe the database
	python ./examples/database/describe_database.py

	# show the database
	python ./examples/database/show_databases.py

	# alther the database
	python ./examples/database/alter_database.py

	# show the database after altered
	python ./examples/database/show_databases.py

	# alter the my_new_database to my_database
	curl $(QUERY_URL) $(CURL_OPTS_ALTER_DATABASE)

	# show the database to check if the database is altered back to my_database
	python ./examples/database/show_databases.py

pre_test: # setup the production server
	sh ./test/pre

.PHONY: test test_schema test_tables test_database test_
