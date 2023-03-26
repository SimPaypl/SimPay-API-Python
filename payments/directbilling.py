from hashlib import sha256
import json
import types
import requests


class DirectBilling:
    def __init__(self, api_key, api_password):
        self.api_key = api_key
        self.api_password = api_password
        self.url = 'https://api.simpay.pl/directbilling'
        self.headers = {
            'X-SIM-KEY': self.api_key,
            'X-SIM-PASSWORD': self.api_password
        }

    # https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-listy-uslug
    def get_service_list(self):
        result = []

        r = requests.get(self.url + '/', headers=self.headers)
        data = r.json()

        result.extend(data.data)

        while data.pagination.links.next_page is not None:
            params = { 'page': data.pagination.current_page + 1 }
            r = requests.get(self.url + '/', headers=self.headers, params=params)
            data = r.json()

            result.extend(data.data)

        return r.json()
    
    def get_service_list_paginated(self, page=None, limit=None):
        params = types.SimpleNamespace()

        if page:
            params.page = page
        if limit:
            params.limit = limit

        r = requests.get(self.url + '/', headers=self.headers, params=params)

        return r.json()
    
    # https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-informacji-o-usludze
    def get_service(self, service_id):
        r = requests.get(self.url + '/' + service_id, headers=self.headers)

        return r.json().data
    
    # https://docs.simpay.pl/pl/python/?python#directbilling-kalkulacja-prowizji
    def calculate_commission(self, service_id, amount):
        r = requests.get(self.url + '/' + service_id + '/calculate?amount=' + amount);

        return r.json().data

    # https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-listy-transakcji
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
    
    # https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-informacji-o-transakcji
    def get_transaction(self, service_id, transaction_id):
        r = requests.get(self.url + '/' + service_id + '/transactions/' + transaction_id, headers=self.headers)

        return r.json().data

    # https://docs.simpay.pl/pl/python/?python#directbilling-generowanie-transakcji
    def create_transaction(self, service_id, key, request):
        request.signature = self.generate_signature(key, request)

        r = requests.post(self.url + '/' + service_id + '/transactions', headers=self.headers, data=json.dumps(request))

        return r.json().data

    # https://docs.simpay.pl/pl/python/?python#directbilling-generowanie-transakcji
    def check_notification(self, key, body):
        if body.signature is None:
            return False
        
        return body.signature == self.generate_signature(key, body)

    # https://docs.simpay.pl/pl/python/?python#directbilling-generowanie-transakcji
    def generate_signature(self, key, data):
        elements = [
            data.amount,
            data.amountType,
            data.description,
            data.control
        ]
        
        if data.returns is not None:
            elements.append(data.returns.success)
            elements.append(data.returns.failure)

        elements.append(data.phoneNumber)
        elements.append(key)

        return sha256(bytes.fromhex([e for e in elements if e is not None].join('|'))).hexdigest()
