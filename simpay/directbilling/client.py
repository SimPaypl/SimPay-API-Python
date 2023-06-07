from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simpay import Client

from hashlib import sha256
from simpay.baseModel import Response, RequestMethod
from simpay.directbilling.models import DCB_Service, DCB_Transaction, DCB_Service_CalculatedCommissions, DCB_Transaction_Returns, DCB_GeneratedTransaction, DCB_Amount_Type


class DirectBillingClient(object):
    def __init__(self, client: 'Client') -> None:
        self._client = client

    def get_services(self) -> list[DCB_Service]:
        return [DCB_Service(**model) for model in self._client.requestAllPages(RequestMethod.GET, 'directbilling')]

    def get_services_paginate(self, page: int = 1, pageSize: int = 15) -> list[DCB_Service]:
        return [DCB_Service(**model) for model in self._client.request(RequestMethod.GET, 'directbilling', options={
            'page': page,
            'limit': pageSize
        })['data']]

    def get_service(self, service_id: str) -> DCB_Service:
        return DCB_Service(**self._client.request(
            RequestMethod.GET, f'directbilling/{service_id}')['data'])

    def get_transactions(self, service_id: str) -> list[DCB_Transaction]:
        return [DCB_Transaction(**model) for model in self._client.requestAllPages(RequestMethod.GET,
                                                                                   f'directbilling/{service_id}/transactions')]

    def get_transactions_paginate(self, service_id: str, page: int = 1, pageSize: int = 15) -> Response[DCB_Transaction]:
        return [DCB_Transaction(**model) for model in self._client.request(RequestMethod.GET,
                                                                           f'directbilling/{service_id}/transactions', options={
                                                                               'page': page,
                                                                               'limit': pageSize
                                                                           })['data']]

    def get_transaction(self, service_id: str, transaction_id: int) -> DCB_Transaction:
        return DCB_Transaction(**self._client.request(RequestMethod.GET,
                                                      f'directbilling/{service_id}/transactions/{transaction_id}')['data'])

    def get_calculate(self, service_id: str, amount: float) -> list[DCB_Service_CalculatedCommissions]:
        return DCB_Transaction(**self._client.request(RequestMethod.GET,
                                                      f'directbilling/{service_id}/calculate/', options={
                                                          'amount': amount
                                                      })['data'])

    def generate_transaction(self, service_id: str, hash: str, amount: float, amountType: DCB_Amount_Type = None, control: str = None, description: str = None, returns: DCB_Transaction_Returns = None, phoneNumber: str = None, steamid: str = None) -> DCB_GeneratedTransaction:
        if not amountType:
            amountType = DCB_Amount_Type.NET
        fields = {
            'amount': amount,
            'amountType': amountType.value,
        }
        signatureBuffer = str(amount) + '|' + amountType.value + '|'
        if description:
            fields['description'] = description
            signatureBuffer += description + '|'
        if control:
            fields['control'] = control
            signatureBuffer += control + '|'
        if returns:
            fields['returns'] = returns
            signatureBuffer += returns + '|'
        if phoneNumber:
            fields['phoneNumber'] = phoneNumber
            signatureBuffer += phoneNumber + '|'
        if steamid:
            fields['steamid'] = steamid
            signatureBuffer += steamid + '|'
        signatureBuffer += hash
        fields['signature'] = sha256(
            signatureBuffer.encode('UTF-8')).hexdigest()

        return DCB_GeneratedTransaction(**self._client.request(RequestMethod.POST,
                                                               f'directbilling/{service_id}/transactions', fields)['data'])

    def verify_transaction(self, fields: dict, hash: str) -> bool:
        signature = fields['signature']
        del fields['signature']
        signatureBuffer = []
        for value in fields.values():
            if isinstance(value, dict):
                for fieldValue in value.values():
                    signatureBuffer.append(str(fieldValue))
            else:
                signatureBuffer.append(str(value))
        signatureBuffer.append(hash)

        return signature == sha256('|'.join(signatureBuffer).encode('UTF-8')).hexdigest()
