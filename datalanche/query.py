# -*- coding: utf-8 -*-
import collections
from expression import DLExpression

class DLQuery(object):
    def __init__(self):
        self.url = '/'
        self.params = collections.OrderedDict()

    #
    # ALTER TABLE
    #

    def alter_table(self, table_name):
        self.url = '/alter_table'
        self.params['table_name'] = table_name
        return self # method chaining
                   
    def add_collaborator(self, username, permission):
        if 'add_collaborators' not in self.params:
            self.params['add_collaborators'] = collections.OrderedDict()
        self.params['add_collaborators'][username] = permission
        return self # method chaining

    def add_column(self, column_name, attributes):
        if 'add_columns' not in self.params:
            self.params['add_columns'] = collections.OrderedDict()
        self.params['add_columns'][column_name] = attributes
        return self # method chaining

    def add_source(self, source_name, attributes):
        if 'add_sources' not in self.params:
            self.params['add_sources'] = collections.OrderedDict()
        self.params['add_sources'][source_name] = attributes
        return self # method chaining
    
    def alter_collaborator(self, username, permission):
        if 'alter_collaborators' not in self.params:
            self.params['alter_collaborators'] = collections.OrderedDict()
        self.params['alter_collaborators'][username] = permission
        return self # method chaining

    def alter_column(self, column_name, attributes):
        if 'alter_columns' not in self.params:
            self.params['alter_columns'] = collections.OrderedDict()
        self.params['alter_columns'][column_name] = attributes
        return self # method chaining

    def alter_source(self, source_name, attributes):
        if 'alter_sources' not in self.params:
            self.params['alter_sources'] = collections.OrderedDict()
        self.params['alter_sources'][source_name] = attributes
        return self # method chaining

    def description(self, text):
        self.params['description'] = text
        return self # method chaining

    def drop_collaborator(self, username):
        if 'drop_collaborators' not in self.params:
            self.params['drop_collaborators'] = list()
        self.params['drop_collaborators'].append(username)
        return self # method chaining

    def drop_column(self, column_name):
        if 'drop_columns' not in self.params:
            self.params['drop_columns'] = list()
        self.params['drop_columns'].append(column_name)
        return self # method chaining

    def drop_source(self, source_name):
        if 'drop_sources' not in self.params:
            self.params['drop_sources'] = list()
        self.params['drop_sources'].append(source_name)
        return self # method chaining

    def is_private(self, boolean):
        self.params['is_private'] = boolean
        return self # method chaining

    def license(self, attributes):
        self.params['license'] = attributes
        return self # method chaining

    def rename_column(self, column_name, new_name):
        if 'rename_columns' not in self.params:
            self.params['rename_columns'] = collections.OrderedDict()
        self.params['rename_columns'][column_name] = new_name
        return self # method chaining

    def rename_source(self, source_name, new_name):
        if 'rename_sources' not in self.params:
            self.params['rename_sources'] = collections.OrderedDict()
        self.params['rename_sources'][source_name] = new_name
        return self # method chaining

    def rename_to(self, table_name):
        self.params['rename_to'] = table_name
        return self # method chaining

    def set_schema(self, schema_name):
        self.params['set_schema'] = schema_name
        return self # method chaining

    #
    # CREATE TABLE
    #

    def create_table (self, definition):
        self.url = '/create_table'
        self.params = definition
        return self # method chaining

    #
    # DELETE
    #

    def delete_from(self, table_name):
        self.url = '/delete'
        self.params['table_name'] = table_name
        return self # method chaining

    # where() defined below

    #
    # DROP TABLE
    #

    def drop_table(self, table_name):
        self.url = '/drop_table'
        self.params['table_name'] = table_name
        return self # method chaining

    #
    # GET TABLE INFO
    #

    def get_table_info(self, table_name):
        self.url = '/get_table_info'
        self.params['table_name'] = table_name
        return self # method chaining

    #
    # GET TABLE LIST
    #

    def get_table_list(self):
        self.url = '/get_table_list'
        return self # method chaining

    #
    # INSERT
    #

    def insert_into(self, table_name):
        self.url = '/insert'
        self.params['table_name'] = table_name
        return self # method chaining

    def values(self, rows):
        self.params['values'] = rows
        return self # method chaining

    #
    # SELECT
    #

    def select(self, columns):
        self.url = '/select'
        self.params['select'] = columns
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

    def limit(self, integer):
        self.params['limit'] = integer
        return self # method chaining

    def offset(self, integer):
        self.params['offset'] = integer
        return self # method chaining

    def order_by(self, expr_array):
        self.params['order_by'] = expr_array
        return self # method chaining

    def total(self, boolean):
        self.params['total'] = boolean
        return self # method chaining

    # where() defined below

    #
    # UPDATE
    #

    def update(self, table_name):
        self.url = '/update'
        self.params['table_name'] = table_name
        return self # method chaining

    def set(self, kv_pairs):
        self.params['set'] = kv_pairs
        return self # method chaining

    # where() defined below

    #
    # COMMON CLAUSES
    #

    def where(self, expression):
        self.params['where'] = expression
        return self # method chaining

    #
    # EXPRESSIONS
    #

    def column(self, column_name):
        return { '$column': column_name }

    #
    # usage examples
    #
    # q.expr(2, "$+", 2)
    # q.expr("$~", 2)
    # q.expr(2, "$!")
    # q.expr(q.column("c1"), "$like", "%abc%")
    # q.expr(q.column("c1"), "$not", "$in", [1, 2, 3, 4])
    # q.expr(q.column("c1"), "$=", 1, "$and", "$c2", "$=", 2)
    #
    def expr(self, *args):
        # *args is a built-in Python variable which is a tuple of function args
        return { '$expr': list(*args) }
        
