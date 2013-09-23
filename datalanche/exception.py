# -*- coding: utf-8 -*-

class DLException(Exception):
    def __init__(self, status_code, body, debug_info):
        self.response = debug_info['response']
        self.response['body'] = debug_info['request']['body']
        del debug_info['request']['body'] # the ['body'] should be in response
        self.request = debug_info['request']
        self.error_message = body['message']
        self.error_type = body['code']
        self.status_code = status_code

        exception = {
            'status_code': self.status_code,
            'error_message' : self.error_message,
            'error_type' : self.error_type,
            'request': self.request,
            'response': self.response
        }
        Exception.__init__(self, exception)



