import json

import pytest
import requests

from simpay import Client, ClientException
from simpay.directbilling.models import DCB_Amount_Type, DCB_Service_Status, DCB_Transaction_Returns, DCB_Transaction_Status


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



def test_generate_transaction_sends_return_urls_as_success_and_failure():
    client, fake = client_with(make_response(200, {
        'success': True,
        'data': {'transactionId': 't1', 'redirectUrl': 'https://db.simpay.pl/t1'},
    }))

    client.DirectBilling.generate_transaction(
        'svc', 'secret-hash', 10,
        returns=DCB_Transaction_Returns(complete='https://shop.example/ok', failure='https://shop.example/fail'))

    assert fake.calls[0]['json']['returns'] == {
        'success': 'https://shop.example/ok',
        'failure': 'https://shop.example/fail',
    }


# Response bodies below follow the resources and controllers in simpay-api.

def test_verify_code_parses_an_unused_code():
    client, fake = client_with(make_response(200, {'success': True, 'data': {
        'used': False, 'code': 'ABC123', 'test': False, 'from': '48123456789', 'number': 7136, 'value': 0.5,
    }}))

    code = client.SMS.verify_code('svc', 'ABC123', 7136)

    assert fake.calls[0]['url'] == 'https://api.simpay.pl/sms/svc'
    assert fake.calls[0]['json'] == {'code': 'ABC123', 'number': 7136}
    assert code.used is False
    assert code.from_number == '48123456789'
    assert code.number == 7136
    assert code.used_at is None


def test_verify_code_parses_an_already_used_code():
    client, _ = client_with(make_response(200, {'success': True, 'data': {
        'used': True, 'code': 'ABC123', 'test': True, 'from': '48123456789', 'number': 7136, 'value': 0.5,
        'used_at': '2026-11-22T10:00:00.000000Z',
    }}))

    code = client.SMS.verify_code('svc', 'ABC123')

    assert code.used is True
    assert code.test is True
    assert code.used_at.isoformat() == '2026-11-22T10:00:00+00:00'


def test_get_calculate_parses_amounts_per_operator():
    client, fake = client_with(make_response(200, {'success': True, 'data': {
        'orange': {'net': 4.07, 'gross': 5.01},
        'play': None,
        't-mobile': {'net': 4.5, 'gross': 5.54},
        'plus': None,
    }}))

    result = client.DirectBilling.get_calculate('svc', 2.5)

    assert fake.calls[0]['url'] == 'https://api.simpay.pl/directbilling/svc/calculate'
    assert fake.calls[0]['params'] == {'amount': 2.5}
    assert result.orange.gross == 5.01
    assert result.tmobile.net == 4.5
    assert result.play is None


def test_get_transaction_parses_directbilling_transaction():
    client, _ = client_with(make_response(200, {'success': True, 'data': {
        'id': 'tx-1',
        'status': 'transaction_db_payed',
        'phoneNumber': 48123456789,
        'control': 'order-15',
        'value': 12.3,
        'value_net': 10,
        'value_created': 10,
        'value_created_type': 'NET',
        'operator': 't-mobile',
        'notify': {'is_send': True, 'last_send_at': '2026-11-22T10:00:00.000000Z', 'count': None},
        'score': None,
        'created_at': '2026-11-22T09:59:00.000000Z',
        'updated_at': '2026-11-22T10:00:00.000000Z',
    }}))

    transaction = client.DirectBilling.get_transaction('svc', 'tx-1')

    assert transaction.status == DCB_Transaction_Status.PAYED
    assert transaction.phoneNumber == '48123456789'
    assert transaction.value_netto == 10
    assert transaction.operator == 't-mobile'
    assert transaction.notify.is_send is True


def test_get_service_parses_operator_keys_and_numeric_commissions():
    client, _ = client_with(make_response(200, {'success': True, 'data': {
        'id': 'svc', 'name': 'Sklep', 'suffix': 'SKLEP', 'status': 'service_active',
        'api': {'complete': 'https://shop.example/ok', 'failure': 'https://shop.example/fail'},
        'providers': {'t-mobile': True, 'orange': True, 'play': False, 'plus': True},
        'commissions': {
            't-mobile': {'commission_0': 45, 'commission_9': 60, 'commission_25': 70},
            'orange': {'commission_0': 45, 'commission_9': 60, 'commission_25': 70},
            'play': {'commission_0': None, 'commission_9': None, 'commission_25': None},
            'plus': {'commission_0': 45, 'commission_9': 60, 'commission_25': 70},
        },
        'maxValues': {'t-mobile': 500, 'orange': 500, 'play': None, 'plus': 500},
        'created_at': '2026-01-01T00:00:00.000000Z',
    }}))

    service = client.DirectBilling.get_service('svc')

    assert service.status == DCB_Service_Status.ACTIVE
    assert service.providers.tmobile is True
    assert service.providers.play is False
    assert service.commissions.tmobile.commission_9 == '60'
    assert service.commissions.play.commission_0 is None
    assert service.maxValues.tmobile == '500'

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


def test_get_services_paginate_parses_list_items_with_every_status():
    statuses = [
        'service_active', 'service_db_new', 'service_db_blocked', 'service_db_deleted',
        'service_db_second_verify', 'service_db_rejected', 'service_verify', 'service_db_ongoing_registration',
    ]
    client, _ = client_with(make_response(200, {'success': True, 'data': [
        {'id': f'svc-{i}', 'name': 'Sklep', 'suffix': 'SKLEP', 'status': status, 'created_at': '2026-01-01T00:00:00+01:00'}
        for i, status in enumerate(statuses)
    ]}))

    services = client.DirectBilling.get_services_paginate()

    assert [service.status.value for service in services] == statuses
    assert services[0].status == DCB_Service_Status.ACTIVE
    assert services[2].status == DCB_Service_Status.BLOCKED
    assert services[0].commissions is None


def test_get_transactions_paginate_parses_sms_transactions():
    client, _ = client_with(make_response(200, {'success': True, 'data': [
        {'id': 123, 'from': 48500111222, 'code': 'ABC123', 'used': True, 'send_at': '2026-01-01T00:00:00+01:00'},
        {'id': 124, 'from': 48500111333, 'code': None, 'used': False, 'send_at': '2026-01-01T00:00:00+01:00'},
    ], 'pagination': {'total': 2, 'count': 2, 'per_page': 15, 'current_page': 1, 'total_pages': 1,
                      'links': {'next_page': None, 'prev_page': None}}}))

    transactions = client.SMS.get_transactions_paginate('svc')

    assert [t.id for t in transactions] == ['123', '124']
    assert transactions[0].from_number == 48500111222
    assert transactions[1].code is None


def test_get_transaction_parses_sms_transaction_details():
    client, _ = client_with(make_response(200, {'success': True, 'data': {
        'id': 125, 'from': 48500111222, 'code': 'ABC123', 'used': True,
        'send_number': 7055, 'value': 0.5, 'send_at': '2026-01-01T00:00:00+01:00',
    }}))

    transaction = client.SMS.get_transaction('svc', 125)

    assert transaction.id == '125'
    assert transaction.send_number == 7055
    assert transaction.value == 0.5
