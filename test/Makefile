
#host api.datalanche.com

all: pre_test test post_test

pre_test: # setup the production server
	sh pre

test: schema table selects index alter_schema database # run examples test
	
schema:
	# schema examples
	# create a schema
	echo
	echo create a schema
	python ../examples/schema/create_schema.py

	# describe the schema
	echo
	echo describe the schema
	python ../examples/schema/describe_schema.py

	# show the created schema
	echo
	echo show schemas created in my_database
	python ../examples/schema/show_schemas.py

table:
	# table examples
	# create a table
	echo
	echo testing creation of a new table with the name of my_table
	python ../examples/table/create_table.py

	# describe the table
	echo
	echo testing description of the table
	python ../examples/table/describe_table.py

	# show the tables in my_database, should return 2 tables
	echo
	echo testing showing the created tables
	python ../examples/table/show_tables.py

	# insert data into my_schema.my_table
	echo
	echo testing insertion of the values into my_table
	python ../examples/table/insert.py

	# update my_schema.my_table
	echo
	echo testing updating my_table
	python ../examples/table/update.py

	# delete my_schema.my_table
	echo
	echo testing deletion of my_table
	python ../examples/table/delete.py

	# alther the table name and the table descriptions
	echo
	echo testing alterring my_table including alterring my_schema to my_new_schema
	python ../examples/table/alter_table.py

	# create table again after altering table.
	echo
	echo create table again so as to test droping table
	python ../examples/table/create_table.py

	# show table to make sure the new table is created before drop
	echo
	echo show table to make sure the new table is created before drop
	python ../examples/table/show_tables.py

	# drop my_schema.my_table
	echo
	echo testing dropping my_table
	python ../examples/table/drop_table.py

	# show table to make sure the new table is created before drop
	echo
	echo show table to make sure the new table is created before drop
	python ../examples/table/show_tables.py

selects:
	# create sample tables for selects
	sh create_sample_tables

	# testing select example
	echo
	echo testing select all example
	python ../examples/table/select_all.py

	# testing select_search example
	echo
	echo testing select search example
	python ../examples/table/select_search.py

	# testing select_join example
	echo
	echo testing select join example
	python ../examples/table/select_join.py

index:
	# create index on my_schema.my_table
	echo
	echo testing creation of index on my_schema.my_table
	python ../examples/index/create_index.py

	# show the tables with index
	echo
	echo testing show tables with created index
	python ../examples/table/describe_table.py

	# drop index on my_schema.my_table
	echo
	echo testing dropping of index on my_schema.my_table
	python ../examples/index/drop_index.py

	# show the tables with dropped index
	echo
	echo testing show tables with dropped index
	python ../examples/table/describe_table.py

	# create index on my_schema.my_table again for testing alterring index
	echo
	echo testing creation of index on my_schema.my_table again testing alterring index
	python ../examples/index/create_index.py

	# show the tables with index
	echo
	echo testing show tables with created index before alterring index
	python ../examples/table/describe_table.py

	# alter index on my_schema.my_table
	echo
	echo testing alterring of index on my_schema.my_table
	python ../examples/index/alter_index.py

	# show the tables with alterred index
	echo
	echo testing show tables with alterred index
	python ../examples/table/describe_table.py

alter_schema:
	#echo drop the schema: my_new_schema before testing alter_schema example
	echo
	echo drop the schema: my_new_schema before testing alter_schema example
	curl https://api.datalanche.com/my_database/query -X POST -u "GoyY7hI2S5igDS4pG2Vdyg==:e02C96sqR5mvUoQXkCC2Gg==" -H "Content-Type: application/json" -d '{
	"drop_schema": "my_new_schema",
	"cascade": true
	}'

	# alter my_schema to my_new_schema
	echo
	echo alter the schema from my_schema to my_new_schema
	python ../examples/schema/alter_schema.py

	# show schema which should show my_new_schema
	echo
	echo testing show schema for making sure schema is alterred.
	python ../examples/schema/show_schemas.py

	#create the schema again to test drop schema.
	echo
	echo create schema again to test dropping schema
	python ../examples/schema/create_schema.py

	# show schema which should show my_schema and my_new_schema
	echo
	echo make sure my_schema is existed.
	python ../examples/schema/show_schemas.py

	# drop my_schema
	echo
	echo testing droping schema
	python ../examples/schema/drop_schema.py

	# show schema which should show new_schema only
	echo
	echo testing show schema for making sure my_schema is dropped.
	python ../examples/schema/show_schemas.py

database:
	# database examples
	# describe the database
	echo
	echo testing describe database
	python ../examples/database/describe_database.py

	# show the database
	echo
	echo testing showing database
	python ../examples/database/show_databases.py

	# alther the database
	echo
	echo testing altering database
	python ../examples/database/alter_database.py

	# show the database after altered
	echo
	echo testing show database, should display my_new_database
	python ../examples/database/show_databases.py

	# alter the my_new_database to my_database
	echo
	echo  alter the my_new_database to my_database
	curl https://api.datalanche.com/query -X POST -u "GoyY7hI2S5igDS4pG2Vdyg==:e02C96sqR5mvUoQXkCC2Gg==" -H "Content-Type: application/json" -d '{
	"alter_database": "my_new_database",
	"rename_to": "my_database"
	}'

	# show the database to check if the database is altered back to my_database
	echo
	echo Make sure the name of my_new_database is changed back to my_database
	python ../examples/database/show_databases.py
