import json

import pytest
import requests

from simpay import Client, ClientException
from simpay.directbilling.models import DCB_Amount_Type


def make_response(status_code, body):
    response = requests.Response()
    response.status_code = status_code
    response._content = json.dumps(body).encode() if body is not None else b''
    return response


class FakeHttp:
    """Replaces requests.Session.request and records every call."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, method, url, params=None, json=None, headers=None):
        self.calls.append({'method': method, 'url': url, 'params': params, 'json': json})
        return self.responses.pop(0)


def client_with(*responses, api_password='test-password'):
    client = Client('test-key', api_password)
    fake = FakeHttp(*responses)
    client._http_client.request = fake
    return client, fake


def page(data, current_page, next_page):
    return make_response(200, {
        'success': True,
        'data': data,
        'pagination': {
            'total': 3, 'count': len(data), 'per_page': 2,
            'current_page': current_page, 'total_pages': 2,
            'links': {'next_page': next_page, 'prev_page': None},
        },
    })


def test_client_sends_api_credentials_as_headers():
    client = Client('test-key', 'test-password')

    assert client._http_client.headers['X-SIM-KEY'] == 'test-key'
    assert client._http_client.headers['X-SIM-PASSWORD'] == 'test-password'


def test_client_omits_password_header_without_password():
    client = Client('test-key', None)

    assert 'X-SIM-PASSWORD' not in client._http_client.headers


def test_api_error_raises_client_exception_with_message():
    client, _ = client_with(make_response(404, {
        'success': False, 'message': 'Service not found', 'errors': {'id': ['missing']},
    }))

    with pytest.raises(ClientException) as error:
        client.SMS.get_service('abc123')

    assert error.value.code == 404
    assert error.value.message == 'Service not found'
    assert error.value.details == {'id': ['missing']}


def test_empty_response_raises_client_exception_with_status():
    client, _ = client_with(make_response(502, None))

    with pytest.raises(ClientException) as error:
        client.SMS.get_service('abc123')

    assert error.value.code == 502


def test_list_methods_fetch_every_page():
    client, fake = client_with(
        page([{'number': 7055, 'value': 0.25, 'value_gross': 0.31, 'adult': False},
              {'number': 7136, 'value': 0.5, 'value_gross': 0.62, 'adult': False}],
             current_page=1, next_page='https://api.simpay.pl/sms/numbers?page=2'),
        page([{'number': 92555, 'value': 12.5, 'value_gross': 15.38, 'adult': True}],
             current_page=2, next_page=None),
    )

    numbers = client.SMS.get_numbers()

    assert [n.number for n in numbers] == [7055, 7136, 92555]
    assert [call['url'] for call in fake.calls] == ['https://api.simpay.pl/sms/numbers'] * 2
    assert fake.calls[1]['params'] == {'page': 2}


def test_generate_transaction_signs_the_request():
    client, fake = client_with(make_response(200, {
        'success': True,
        'data': {'transactionId': 't1', 'redirectUrl': 'https://simpay.pl/pay/t1'},
    }))

    transaction = client.DirectBilling.generate_transaction(
        'svc', 'secret-hash', 10, control='order-1')

    assert transaction.redirectUrl == 'https://simpay.pl/pay/t1'
    assert fake.calls[0]['method'] == 'post'
    assert fake.calls[0]['url'] == 'https://api.simpay.pl/directbilling/svc/transactions'
    assert fake.calls[0]['json'] == {
        'amount': 10,
        'amountType': DCB_Amount_Type.NET.value,
        'control': 'order-1',
        # sha256('10|net|order-1|secret-hash')
        'signature': 'da558ab7a38cf6755be430946e3c6fe348c69d6d870fedb98494742458133eb9',
    }


def notification(signature):
    return {
        'id': 't1',
        'service_id': 'svc',
        'status': 'ok',
        'values': {'net': 1, 'gross': 1.23},
        'signature': signature,
    }


def test_verify_transaction_accepts_a_valid_signature():
    client = Client('test-key', 'test-password')
    # sha256('t1|svc|ok|1|1.23|secret-hash')
    valid = '2edd91d4c2ea7a8396c6f2bd7e133c2d4c75c9ab6e464afda6a30caa792a6773'

    assert client.DirectBilling.verify_transaction(notification(valid), 'secret-hash') is True


def test_verify_transaction_rejects_a_wrong_hash():
    client = Client('test-key', 'test-password')
    valid = '2edd91d4c2ea7a8396c6f2bd7e133c2d4c75c9ab6e464afda6a30caa792a6773'

    assert client.DirectBilling.verify_transaction(notification(valid), 'other-hash') is False


def sms_xml_request(sign):
    return {
        'sms_id': '1',
        'sms_text': 'TEXT',
        'sms_from': '48500',
        'send_number': '7055',
        'send_time': '2026-01-01',
        'sign': sign,
    }


def test_sms_xml_accepts_a_correctly_signed_request():
    client = Client('test-key', None)
    # sha256('1' + 'TEXT' + '48500' + '7055' + '2026-01-01' + 'test-key')
    sign = '13ce9728f3a2f5efc06d947a9967e442db068a927b759c7f140e44f54d58bcac'

    assert client.SMS_XML.check_parameters(sms_xml_request(sign)) is True


def test_sms_xml_rejects_a_tampered_request():
    client = Client('test-key', None)
    request = sms_xml_request('13ce9728f3a2f5efc06d947a9967e442db068a927b759c7f140e44f54d58bcac')
    request['send_number'] = '92555'

    assert client.SMS_XML.check_parameters(request) is False
