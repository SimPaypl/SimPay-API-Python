import json
import types
import requests


class SMS:
    def __init__(self, api_key, api_password):
        self.api_key = api_key
        self.api_password = api_password
        self.url = 'https://api.simpay.pl/sms'
        self.headers = {
            'X-SIM-KEY': self.api_key,
            'X-SIM-PASSWORD': self.api_password
        }

    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-listy-uslug
    def get_service_list(self):
        result = []

        r = requests.get(self.url, headers=self.headers)
        data = r.json()

        result.extend(data.data)

        while data.pagination.links.next_page is not None:
            params = { 'page': data.pagination.current_page + 1 }
            r = requests.get(self.url, headers=self.headers, params=params)
            data = r.json()

            result.extend(data.data)

        return r.json()
    
    def get_service_list_paginated(self, page=None, limit=None):
        params = types.SimpleNamespace()

        if page:
            params.page = page
        if limit:
            params.limit = limit

        r = requests.get(self.url, headers=self.headers, params=params)

        return r.json()
    
    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-informacji-o-usludze
    def get_service(self, service_id):
        r = requests.get(self.url + '/' + service_id, headers=self.headers)

        return r.json().data
    
    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-listy-transakcji
    def get_transaction_list(self, service_id):
        result = []

        r = requests.get(self.url + '/' + service_id + '/transactions', headers=self.headers)
        data = r.json()

        result.extend(data.data)

        while data.pagination.links.next_page is not None:
            params = { 'page': data.pagination.current_page + 1 }
            r = requests.get(self.url + '/' + service_id + '/transactions', headers=self.headers, params=params)
            data = r.json()

            result.extend(data.data)

        return r.json()
    
    def get_transaction_list_paginated(self, service_id, page=None, limit=None):
        params = types.SimpleNamespace()

        if page:
            params.page = page
        if limit:
            params.limit = limit

        r = requests.get(self.url + '/' + service_id + '/transactions', headers=self.headers, params=params)

        return r.json()
    
    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-informacji-o-transakcji
    def get_transaction(self, service_id, transaction_id):
        r = requests.get(self.url + '/' + service_id + '/transactions/' + transaction_id, headers=self.headers)

        return r.json().data

    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-dostepnych-numerow-dla-uslugi
    def get_service_numbers(self, service_id):
        result = []

        r = requests.get(self.url + '/sms/' + service_id + '/numbers', headers=self.headers)
        data = r.json()

        result.extend(data.data)

        while data.pagination.links.next_page is not None:
            params = { 'page': data.pagination.current_page + 1 }
            r = requests.get(self.url + '/sms/' + service_id + '/numbers', headers=self.headers, params=params)
            data = r.json()

            result.extend(data.data)

        return r.json()

    def get_service_numbers_paginated(self, service_id, page=None, limit=None):
        params = types.SimpleNamespace()

        if page:
            params.page = page
        if limit:
            params.limit = limit

        r = requests.get(self.url + '/sms/' + service_id + '/numbers', headers=self.headers, params=params)

        return r.json()
    
    # https://docs-new.simpay.pl/python/?python#sms-informacji-o-pojedynczym-numerze-uslugi
    def get_service_number(self, service_id, number):
        r = requests.get(self.url + '/sms/' + service_id + '/numbers/' + number, headers=self.headers)

        return r.json().data

    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-wszystkich-dostepnych-numerow
    def get_numbers(self):
        result = []

        r = requests.get(self.url + '/numbers', headers=self.headers)
        data = r.json()

        result.extend(data.data)

        while data.pagination.links.next_page is not None:
            params = { 'page': data.pagination.current_page + 1 }
            r = requests.get(self.url + '/numbers', headers=self.headers, params=params)
            data = r.json()

            result.extend(data.data)

        return r.json()
    
    def get_numbers_paginated(self, page=None, limit=None):
        params = types.SimpleNamespace()

        if page:
            params.page = page
        if limit:
            params.limit = limit

        r = requests.get(self.url + '/numbers', headers=self.headers, params=params)

        return r.json()
    
    # https://docs-new.simpay.pl/python/?python#sms-pobieranie-pojedynczego-numeru-sms

    def get_number(self, number):
        r = requests.get(self.url + '/numbers/' + number, headers=self.headers)

        return r.json().data

    # https://docs-new.simpay.pl/python/?python#sms-weryfikacja-poprawnosci-kodu

    def verify_sms_code(self, service_id, code, number=None):
        body = types.SimpleNamespace()
        body.code = code

        if number:
            body.number = number

        r = requests.post(self.url + '/' + service_id, headers=self.headers, data=json.dumps(body))

        return r.json().data

