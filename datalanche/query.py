# -*- coding: utf-8 -*-
import collections

class DLQuery(object):

    def __init__(self, database = None):
        self.params = collections.OrderedDict()
        if database != None:
            self.params['database'] = database

    #
    # COMMON
    #

    def cascade(self, boolean):
        self.params['cascade'] = boolean
        return self # method chaining

    def columns(self, columns):
        self.params['columns'] = columns
        return self # method chaining

    def description(self, text):
        self.params['description'] = text
        return self # method chaining

    def rename_to(self, table_name):
        self.params['rename_to'] = table_name
        return self # method chaining

    def where(self, expression):
        self.params['where'] = expression
        return self # method chaining

    #
    # EXPRESSIONS
    #

    #
    # usage examples
    #
    # q.expr(2, "+", 2)
    # q.expr("~", 2)
    # q.expr(2, "!")
    # q.expr(q.column("c1"), "$like", "%abc%")
    # q.expr(q.column("c1"), "$not", "$in", [1, 2, 3, 4])
    # q.expr(q.column("c1"), "=", 1, "$and", q.column("c2"), "=", 2)
    #
    def expr(self, *args):
        # *args is a built-in Python variable which is a tuple of function args
        return { '$expr': list(args) }

    def alias(self, alias_name):
        return { '$alias': alias_name }

    def column(self, column_name):
        return { '$column': column_name }

    def literal(self, value):
        return { '$literal': value }

    def table(self, table_name):
        return { '$table': table_name }

    #
    # FUNCTIONS
    #

    # NOTE: *args is a built-in Python variable which is a tuple of function args

    #
    # usage examples
    #
    # q.func("$count", "*")
    # q.func("$sum", q.column("c1"))
    #
    def func(self, *args):
        return { '$function': list(args) }

    def avg(self, *args):
        temp_args = [ '$avg' ] + list(args)
        return { '$function': temp_args }

    def count(self, *args):
        temp_args = [ '$count' ] + list(args)
        return { '$function': temp_args }

    def max(self, *args):
        temp_args = [ '$max' ] + list(args)
        return { '$function': temp_args }

    def min(self, *args):
        temp_args = [ '$min' ] + list(args)
        return { '$function': temp_args }

    def sum(self, *args):
        temp_args = [ '$sum' ] + list(args)
        return { '$function': temp_args }

    #
    # ALTER DATABASE
    #

    def alter_database(self, database_name):
        self.params['alter_database'] = database_name
        return self # method chaining

    def add_collaborator(self, username, permission):
        if 'add_collaborators' not in self.params:
            self.params['add_collaborators'] = collections.OrderedDict()
        self.params['add_collaborators'][username] = permission
        return self # method chaining

    def alter_collaborator(self, username, permission):
        if 'alter_collaborators' not in self.params:
            self.params['alter_collaborators'] = collections.OrderedDict()
        self.params['alter_collaborators'][username] = permission
        return self # method chaining

    def drop_collaborator(self, username):
        if 'drop_collaborators' not in self.params:
            self.params['drop_collaborators'] = list()
        self.params['drop_collaborators'].append(username)
        return self # method chaining

    def is_private(self, boolean):
        self.params['is_private'] = boolean
        return self # method chaining

    def max_size_gb(self, integer):
        self.params['max_size_gb'] = integer
        return self # method chaining

    #
    # ALTER INDEX
    #

    def alter_index(self, index_name):
        self.params['alter_index'] = index_name
        return self # method chaining

    #
    # ALTER SCHEMA
    #

    def alter_schema(self, schema_name):
        self.params['alter_schema'] = schema_name
        return self # method chaining

    #
    # ALTER TABLE
    #

    def alter_table(self, table_name):
        self.params['alter_table'] = table_name
        return self # method chaining

    def add_column(self, column_name, attributes):
        if 'add_columns' not in self.params:
            self.params['add_columns'] = collections.OrderedDict()
        self.params['add_columns'][column_name] = attributes
        return self # method chaining

    # TODO: add_constraint
    
    def alter_column(self, column_name, attributes):
        if 'alter_columns' not in self.params:
            self.params['alter_columns'] = collections.OrderedDict()
        self.params['alter_columns'][column_name] = attributes
        return self # method chaining

    def drop_column(self, column_name, cascade = False):
        if 'drop_columns' not in self.params:
            self.params['drop_columns'] = list()

        column_obj = collections.OrderedDict()
        column_obj['name'] = column_name
        column_obj['cascade'] = cascade
        self.params['drop_columns'].append(column_obj)
        return self # method chaining

    # TODO: drop_constraint

    def rename_column(self, column_name, new_name):
        if 'rename_columns' not in self.params:
            self.params['rename_columns'] = collections.OrderedDict()
        self.params['rename_columns'][column_name] = new_name
        return self # method chaining

    # TODO: rename_constraint

    def set_schema(self, schema_name):
        self.params['set_schema'] = schema_name
        return self # method chaining

    #
    # CREATE INDEX
    #

    def create_index(self, index_name):
        self.params['create_index'] = index_name
        return self # method chaining

    def on_table(self, tableName):
        self.params['on_table'] = tableName
        return self # method chaining

    def unique(self, boolean):
        self.params['unique'] = boolean
        return self # method chaining

    def using_method(self, text):
        self.params['using_method'] = text
        return self # method chaining

    #
    # CREATE SCHEMA
    #

    def create_schema(self, schema_name):
        self.params['create_schema'] = schema_name
        return self # method chaining

    #
    # CREATE TABLE
    #

    def create_table(self, table_name):
        self.params['create_table'] = table_name
        return self # method chaining

    # TODO: constraints

    #
    # DELETE
    #

    def delete_from(self, table_name):
        self.params['delete_from'] = table_name
        return self # method chaining

    #
    # DESCRIBE DATABASE
    #

    def describe_database(self, database_name):
        self.params['describe_database'] = database_name
        return self # method chaining

    #
    # DESCRIBE SCHEMA
    #

    def describe_schema(self, schema_name):
        self.params['describe_schema'] = schema_name
        return self # method chaining

    #
    # DESCRIBE TABLE
    #

    def describe_table(self, table_name):
        self.params['describe_table'] = table_name
        return self # method chaining

    #
    # DROP INDEX
    #

    def drop_index(self, index_name):
        self.params['drop_index'] = index_name
        return self # method chaining

    #
    # DROP SCHEMA
    #

    def drop_schema(self, schema_name):
        self.params['drop_schema'] = schema_name
        return self # method chaining

    #
    # DROP TABLE
    #

    def drop_table(self, table_name):
        self.params['drop_table'] = table_name
        return self # method chaining

    #
    # INSERT
    #

    def insert_into(self, table_name):
        self.params['insert_into'] = table_name
        return self # method chaining

    def values(self, rows):
        self.params['values'] = rows
        return self # method chaining

    #
    # SELECT
    #

    def select(self, columns):
        if columns == '*':
            raise Exception('please use select_all() instead of select("*")')
        self.params['select'] = columns
        return self # method chaining

    def select_all(self):
        self.params['select'] = True
        return self # method chaining

    def distinct(self, boolean):
        self.params['distinct'] = boolean
        return self # method chaining

    def from_tables(self, tables):
        self.params['from'] = tables
        return self # method chaining

    def group_by(self, columns):
        self.params['group_by'] = columns
        return self # method chaining

    def having(self, expression):
        self.params['having'] = expression
        return self # method chaining

    def limit(self, integer):
        self.params['limit'] = integer
        return self # method chaining

    def offset(self, integer):
        self.params['offset'] = integer
        return self # method chaining

    def order_by(self, expr_array):
        self.params['order_by'] = expr_array
        return self # method chaining

    def search(self, query_text):
        self.params['search'] = query_text
        return self # method chaining

    #
    # SHOW DATABASES
    #

    def show_databases(self):
        self.params['show_databases'] = True
        return self # method chaining

    #
    # SHOW SCHEMAS
    #

    def show_schemas(self):
        self.params['show_schemas'] = True
        return self # method chaining

    #
    # SHOW TABLES
    #

    def show_tables(self):
        self.params['show_tables'] = True
        return self # method chaining

    #
    # UPDATE
    #

    def update(self, table_name):
        self.params['update'] = table_name
        return self # method chaining

    def set(self, kv_pairs):
        self.params['set'] = kv_pairs
        return self # method chaining        
