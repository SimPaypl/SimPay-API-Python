from .__version__ import VERSION
from simpay.baseModel import RequestMethod, Response
from simpay.sms.client import SMSClient
from simpay.directbilling.client import DirectBillingClient
import requests


class ClientException(Exception):
    def __init__(self, code=200, message=None, details=None):
        self.code = code
        self.message = message
        self.details = details
    
    def __str__(self):
        return self.message


class Client(object):
    _version = VERSION
    _user_agent = 'simpay-python-api'
    _base_endpoint = 'https://api.simpay.pl/'

    def __init__(
        self,
        api_key: str,
        api_password: str | None,
        timeout: int = 5
    ) -> None:
        self.api_key = api_key
        self.api_password = api_password
        self.timeout = timeout

        self._http_client = requests.Session()
        self._http_client.mount(self._base_endpoint,
                                requests.adapters.HTTPAdapter())
        self._http_client.headers['accept'] = 'application/json'
        self._http_client.headers['content-type'] = 'application/json'
        self._http_client.headers['user-agent'] = self._user_agent
        self._http_client.headers['X-SIM-KEY'] = self.api_key

        if self.api_password is not None:
            self._http_client.headers['X-SIM-PASSWORD'] = self.api_password

        self.SMS: SMSClient = SMSClient(self)
        self.DirectBilling: DirectBillingClient = DirectBillingClient(self)

    def request(self, method: RequestMethod, uri: str, fields: dict[str, any] | None = None, headers: dict[str, any] | None = None, options: dict[str, any] | None = None) -> Response:
        response = self._http_client.request(
            method.value, self._base_endpoint + uri, params=options, json=fields, headers=headers)
        if len(response.content) == 0:
            raise ClientException(response.status_code)
        if not response.ok:
            responseBody = response.json()
            if responseBody['message']:
                raise ClientException(response.status_code, responseBody['message'], responseBody['errors'])
            else:
                raise ClientException(response.status_code)
        return response.json()

    def requestAllPages(self, method: RequestMethod, uri: str, fields: dict[str, any] | None = None, headers: dict[str, any] | None = None, options: dict[str, any] | None = None) -> object:
        response = self.request(method, uri, fields, headers, options)
        responseData = []
        if response['success']:
            responseData = responseData + response['data']
            while response['pagination']['links']['next_page']:
                response = self.request(
                    method, uri, fields, headers, options.update({
                        'page': response['pagination']['current_page'] + 1
                    }))
                if response['success']:
                    responseData = responseData + response['data']

        return responseData
