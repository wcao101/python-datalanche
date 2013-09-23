# -*- coding: utf-8 -*-

class DLException(Exception):
    def __init__(self, status_code, response, debug_info):
        self.response = {}
        self.status_code = status_code
        self.response['body'] = debug_info['request']['body']
        self.response['http_status'] = debug_info['response']['http_status']
        self.response['headers'] = debug_info['response']['headers']
        self.request = debug_info['request']
        self.error_message = response['message']
        self.error_type = response['code']
        exception = {
            'status_code': status_code,
            'error_message' : response['message'],
            'error_type' : response['code']
        }
        Exception.__init__(self, exception)



