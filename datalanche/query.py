# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
from exception import DLException
from requests.auth import HTTPBasicAuth


class DLQuery(object):
    def __init__(self):
        self.url_type = 'get'
        self.base_url = '/'
        self.params = {
            'add_columns' : None,
            'alter_columns' : None,
            'columns' : None,
            'debug' : None,
            'description' : None,
            'distinct' : None,
            'drop_columns' : None,
            'from' : None,
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

    def add_column(self,columns):
        
        if self.params['add_columns'] == None:
            self.params['add_columns'] = []
            self.params['add_columns'].append(columns)

        return self
    
    def alter_column(self,column_name, column_object):
        
        if self.params['alter_columns'] == None:
            self.params['alter_columns'] ={}
        self.params['alter_columns']['column_name'] = column_object

        return self

    def alter_table(self, table_name):
        
        self.url_type = 'post'
        self.base_url = '/alter_table'
        self.params['name'] = table_name
        
        return self
        
    def columns(self,object_array):
        
        self.params['columns'] = object_array
        
        return self

    def create_table (self,table_name):
        
        self.url_type = 'post'
        self.base_url = '/create_table'
        self.params['name'] = table_name
        
        return self

    def debug(self,bool):
        
        self.params['debug'] = bool

        return self

    def delete_from(self,table_name):

        self.url_type = 'post'
        self.base_url = '/delete_from'
        self.params['name'] = table_name

        return self

    def description(self,text):
        
        self.params['description'] = text
        
        return self

    def distinct(self,bool):
        
        self.params['distinct'] = bool

        return self

    def drop_column(self,column_name):

        if(self.params['drop_columns'] == None):
            self.params['drop_columns'] = []
        
        self.params['drop_columns'].append(column_name)

        return self

    def drop_table(self,table_name):

        self.url_type = 'del'
        self.base_url = '/drop_table'
        self.params['name'] = table_name

        return self

    def from_table(self,tables):
        
        self.params['from_table'] = tables

        return self

    def get_table_info(self,table_name):

        self.url_type = 'get'
        self.base_url = '/get_table_info'
        self.params['name'] = table_name

        return self

    def get_table_list(self):
        
        self.url_type = 'get'
        self.base_url = '/get_table_list'

        return self

    def group_by(self,columns):

        self.params['group_by'] = columns

        return self

    def insert_into(self,table_name):

        self.url_type = 'post'
        self.base_url = '/insert_into'

        return self

    def is_private(self,bool):
        
        self.params['is_private'] = bool

        return self

    def license(self,license_object):
        
        self.params['license'] = license_object

        return self

    def limit(self,integer):
        
        self.params['limit'] = integer

        return self

    def offset(self,integer):

        self.params['offset'] = integer

        return self

    def order_by(self,object_array):
        
        self.params['order_by'] = object_array

        return self

    def rename(self,table_name):

        self.params['rename'] = table_name

        return self

    def select(self,columns):

        self.url_type = 'post'
        self.base_url = '/select_from'
        self.params['select'] = columns

        return self

    def set(self,form_map):

        self.params['set'] = form_map

        return self

    def sources(self,object_array):
        
        self.params['sources'] = object_array

        return self

    def total(self,bool):
        
        self.params['total'] = bool

        return self

    def update(self,table_name):

        self.url_type = 'post'
        self.base_url = '/update'
        self.params['name'] = table_name

        return self

    def values(self,rows):

        self.params['values'] = rows

        return self

    def where(self,query_filter):
        
        self.params['where'] = query_filter

        return self
        