from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simpay import Client

from simpay.baseModel import Response, RequestMethod
from simpay.sms.models import SMS_Service, SMS_Transaction, SMS_Number


class SMSClient(object):
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def get_services(self) -> list[SMS_Service]:
        return [SMS_Service(**model) for model in self._client.requestAllPages(RequestMethod.GET, 'sms')]

    def get_services_paginate(self, page: int = 1, pageSize: int = 15) -> list[SMS_Service]:
        return [SMS_Service(**model) for model in self._client.request(RequestMethod.GET, 'sms', options={
            'page': page,
            'limit': pageSize
        })['data']]

    def get_service(self, service_id: str) -> SMS_Service:
        return SMS_Service(**self._client.request(
            RequestMethod.GET, f'sms/{service_id}')['data'])

    def get_transactions(self, service_id: str) -> list[SMS_Transaction]:
        return [SMS_Transaction(**model) for model in self._client.requestAllPages(RequestMethod.GET,
                                                                                   f'sms/{service_id}/transactions')]

    def get_transactions_paginate(self, service_id: str, page: int = 1, pageSize: int = 15) -> Response[SMS_Transaction]:
        return [SMS_Transaction(**model) for model in self._client.request(RequestMethod.GET,
                                                                           f'sms/{service_id}/transactions', options={
                                                                               'page': page,
                                                                               'limit': pageSize
                                                                           })['data']]

    def get_transaction(self, service_id: str, transaction_id: int) -> SMS_Transaction:
        return SMS_Transaction(**self._client.request(RequestMethod.GET,
                                                      f'sms/{service_id}/transactions/{transaction_id}')['data'])

    def get_service_numbers(self, service_id: str) -> list[SMS_Number]:
        return [SMS_Number(**model) for model in self._client.requestAllPages(RequestMethod.GET,
                                                                              f'sms/{service_id}/numbers')]

    def get_service_number(self, service_id: str, number: int) -> SMS_Number:
        return SMS_Number(**self._client.request(RequestMethod.GET,
                                                 f'sms/{service_id}/numbers/{number}')['data'])

    def get_numbers(self) -> list[SMS_Number]:
        return [SMS_Number(**model) for model in self._client.requestAllPages(RequestMethod.GET,
                                                                              'sms/numbers')]

    def get_number(self, number: int) -> SMS_Number:
        return SMS_Number(**self._client.request(RequestMethod.GET,
                                                 f'sms/numbers/{number}')['data'])

    def verify_code(self, service_id: str, code: str, number: int = None) -> SMS_Transaction:
        fields = {
            'code': code,
        }

        if number:
            fields['number'] = number

        return SMS_Transaction(**self._client.request(RequestMethod.POST,
                                                      f'sms/{service_id}', fields)['data'])
