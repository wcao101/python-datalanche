# -*- coding: utf-8 -*-

class DLException(Exception):
    def __init__(self, status_code, response, debug_info):
        self.status_code = status_code
        self.response = response
        self.request_info = debug_info['request']
        self.response_info = debug_info['response']
        self.error_message = response['message']
        self.error_type = response['code']
        self.info = {
            'status_code': status_code,
            'request_info' : debug_info['request'],
            'response_info' : debug_info['response'],
            'error_message' : response['message'],
            'error_type' : response['code']
        }
        exception = {
            'status_code': status_code,
            'request_info' : debug_info['request'],
            'response_info' : debug_info['response'],
            'error_message' : response['message'],
            'error_type' : response['code']
        }
        Exception.__init__(self, exception)



