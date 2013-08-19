# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
from exception import DLException
from requests.auth import HTTPBasicAuth


class Query(object):
    def __init__(self):
        self.url_type = 'get'
        self.base_url = '/'
        self.params = {
            'add_columns' : None,
            'alter_columns' : None,
            'columns' : None,
            'debug' : None,
            'description' : None,
            'drop_columns' : None,
            'from_table' : None,
            'group_by' : None,
            'is_private' : None,
            'license' : None,
            'limit' : None,
            'offset' : None,
            'order_by' : None,
            'name' : None,
            'rename' : None,
            'select' : None,
            'set' : None,
            'sorce' : None,
            'total' : None,
            'values' : None,
            'where' : None,
        }

    def add_columns(self,columns):
        
        if self.params['add_columns'] == None:
            self.params['add_columns'] = []
            self.params['add_columns'].append(columns)

        return self
    
    def alter_columnsf(self,column_name, column_object):
        
        if self.params['alter_columns'] == None:
            self.params['alter_columns'] ={}
        self.params['alter_columns']['column_name'] = column_object

        return self

    def alter_table(self, table_name):
        
        self.urlType = 'post'
        self.base_url = '/delete_from'
        self.params['name'] = table_name
        
        return self
        
    def columns(object_array):
        
        self.params['columns'] = object_array
        
        return self

    def create_table (table_name):
        
        self.url_type = 'post'
        self.base_url = '/create_table'
        self.params['name'] = table_name
        
        return self

    def debug(bool):
        
        self.params['debug'] = bool

        return self

    def delete_from(table_name):

        self.url_type = 'post'
        self.base_url = '/delete_from'
        self.params['name'] = table_name

        return self

    def description(text):
        
        self.params['description'] = text
        
        return self

    def distinct(bool):
        
        self.params['distinct'] = bool

        return self

    def drop_column(column_name):

        if(self.params['drop_column'] == None):
            self.params['drop_column'] = []
        
        self.params['drop_column'].append(column_name)

        return self

    def drop_table(table_name):

        self.url_type = 'del'
        self.base_url = '/drop_table'
        self.params['name'] = table_name

        return self

    def from_table(tables):
        
        self.params['from_table'] = tables

        return self

    def get_table_info(table_name):

        self.url_type = 'get'
        self.base_url = '/get_table_info'
        self.params['name'] = table_name

        return self

    def get_table_list():
        
        self.url_type = 'get'
        self.base_url = '/get_table_list'

        return self

    def group_by(columns):

        self.params['group_by'] = columns

        return self

    def insert_into(table_name):

        self.url_type = 'post'
        self.base_url = '/insert_into'

        return self

    def is_private(bool):
        
        self.params['is_private'] = bool

        return self

    def license(license_object):
        
        self.params['license'] = license_object

        return self

    def limit(integer):
        
        self.params['limit'] = integer

        return self

    def offset(integer):

        self.params['offset'] = integer

        return self

    def order_by(object_array):
        
        self.params['order_by'] = object_array

        return self

    def rename(table_name):

        self.params['rename'] = table_name

        return self

    def select(columns):

        self.url_type = 'post'
        self.base_url = '/select_from'
        self.params['select'] = columns

        return self

    def set(form_map):

        self.params['set'] = form_map

        return self

    def sources(object_array):
        
        self.params['sources'] = object_array

        return self

    def total(bool):
        
        self.params['total'] = bool

        return self

    def update(table_name):

        self.url_type = 'post'
        self.base_url = '/update'
        self.params['name'] = table_name

        return self

    def values(rows):

        self.params['values'] = rows

        return self

    def where(query_filter):
        
        self.params['where'] = query_filter

        return self
        
