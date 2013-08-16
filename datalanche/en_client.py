# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
from exception import DLException
from requests.auth import HTTPBasicAuth

def is_boolean(s):
    if s == True or s == False:
        return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def is_string(s):
    return isinstance(s, basestring)

# handle cases where value may not be a list of strings
def list2str(value):
    newstr = ''

    if is_boolean(value):
        newstr = str(value).lower()
    elif is_number(value) or is_string(value):
        newstr = str(value)
    else:
        for i in range(0, len(value)):
            if is_boolean(value[i]):
                newstr = newstr + str(value[i]).lower()
            else:
                newstr = newstr + str(value[i])

            if i < len(value) - 1:
                newstr = newstr + ','
    
    return newstr

class DLClient(object):
    def __init__(
        self, key = '', secret = '', 
        host = None, port = None, verify_ssl = True
    ):
        self.auth_key = key
        self.auth_secret = secret
        self.client = requests.Session()
        self.url = 'https://api.datalanche.com'
        self.verify_ssl = verify_ssl
        if host != None:
            self.url = 'https://' + host
        if port != None:
            self.url = self.url + ':' + str(port)

    def query(self,q = None):
        
        if (q == None):
           pirnt"Error: query is None."
           return self
           
        if (q.url_type == 'del'):
            self.client.delete(
            get_url(q),
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
            )

        elif (q.url_type = 'post'):
            self.client.post(
            get_url(q),
            get_body(q),
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
            )
            
        elif (q.url_type = 'get'):
            self.client.get(
            get_url(q),
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
            )

        else:
            raise DLException(r.status_code, r.json(), r.url)

def get_body(query = None):

    body = {}
    
    if(query == None):
        return body

    if(type(query.debug) == type(True) && query.debug != None):
        body['debug'] = query.debug
        
    if(query.base_url == '/alter_table'):
        
        if(query.add_columns != None):
            body['add_columns'] = query.add_columns
            
        if(query.alter_columns != None):
            body['alter_columns'] = query.alter_columns

        if(query.name != None):
            body['name'] = query.name
            
        if(query.description != None):
            body['description'] = query.description

        if(query.drop_columns != None):
            body['drop_columns'] = query.drop_columns

        if(query.is_private != None):
            body['is_private'] = query.is_private

        if(query.license != None):
            body['license'] = query.license

        if(query.rename != None):
            body['rename'] = query.rename

        if(query.sources != None):
            body['sources'] = query.sources
        
    elif(query.base_url == '/create_table'):
        
         if (query.columns != None):
            body['columns'] = query.columns
        
        if (query.name != None):
            body['name'] = query.name;
        
        if (query.description != None):
            body['description'] = query.description;
                
        if (query.is_private != None) 
            body['is_private'] = query.is_private;
        
        if (query.license != None) 
            body['license'] = query.license;
        
        if (query.sources != None):
            body['sources'] = query.sources;
        
            
