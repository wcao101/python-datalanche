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
        self.add_columns = None
        self.alter_columns = None
        self.columns = None
        self.debug = None
        self.description = None
        self.drop_columns = None
        self.from_table = None
        self.group_by = None
        self.is_private = None
        self.license = None
        self.limit = None
        self.offset = None
        self.order_by = None
        self.name = None
        self.rename = None
        self.select = None
        self.set = None
        self.sorce = None
        self.total = None
        self.values = None
        self.where = None

    def add_columns(self,columns):
        
        if add_columns == None:
            self.add_columns = []
            self.add_columns.append(columns)

        return self
    
    def alter_columnsf(self,column_name, column_object):
        
        if self.alter_columns == None:
            self.alter_columns ={}
        alter_columns['column_name'] = column_object

        return self

    def alter_table(self, table_name):
        
        self.urlType = 'post'
        self.base_url = '/delete_from'
        self.name = table_name
        
        return self
        
    def columns(object_array):
        
        self.columns = object_array
        
        return self

    def create_table (table_name):
        
        self.url_type = 'post'
        self.base_url = '/create_table'
        self.name = table_name
        
        return self

    def debug(bool):
        
        self.debug = bool

        return self

    def delete_from(table_name):

        self.url_type = 'post'
        self.base_url = '/delete_from'
        self.name = table_name

        return self

    def description(text):
        
        self.description = text
        
        return self

    def distinct(bool):
        
        self.distinct = bool

        return self

    def drop_column(column_name):

        if(self.drop_column == None):
            self.drop_column = []
        
        self.drop_column.append(column_name)

        return self

    def drop_table(table_name):

        self.url_type = 'del'
        self.base_url = '/drop_table'
        self.name = table_name

        return self

    def from_table(tables):
        
        self.from_table = tables

        return self

    def get_table_info(table_name):

        self.url_type = 'get'
        self.base_url = '/get_table_info'
        self.name = table_name

        return self

    def get_table_list():
        
        self.url_type = 'get'
        self.base_url = '/get_table_list'

        return self

    def group_by(columns):

        self.group_by = columns

        return self

    def insert_into(table_name):

        self.url_type = 'post'
        self.base_url = '/insert_into'

        return self

    def is_private(bool):
        
        self.is_private = bool

        return self

    def license(license_object):
        
        self.license = license_object

        return self

    def limit(integer):
        
        self.limit = integer

        return self

    def offset(integer):

        self.offset = integer

        return self

    def order_by(object_array):
        
        self.order_by = object_array

        return self

    def rename(table_name):

        self.rename = table_name

        return self

    def select(columns):

        self.url_type = 'post'
        self.base_url = '/select_from'
        self.select = columns

        return self

    def set(form_map):

        self.set = form_map

        return self

    def sources(object_array):
        
        self.sources = object_array

        return self

    def total(bool):
        
        self.total = bool

        return total

    def update(table_name):

        self.url_type = 'post'
        self.base_url = '/update'
        self.name = table_name

        return self

    def values(rows):

        self.values = rows

        return self

    def where(query_filter):
        
        self.where = query_filter

        return self
        
