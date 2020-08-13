from payments.direct_billing import DirectBilling

db = DirectBilling("XXXXXXXXXXXXXXX", "XXXXXXXXXXX", True, "130")


def test_generate_transaction():
    response = db.generate_transaction(api_key="XXXXXXXXXXXX",request={"control": "XXXXXX", "amount": 10.00})
    return response


def test_get_transaction(name):
    response = db.get_transaction(request={"id": name})
    print(response)


def test_get_services():
    response = db.get_services(request={})
    print(response)


def test_get_transaction_limits():
    response = db.get_transaction_limits(request={})
    print(response)


def test_get_service_commission():
    response = db.get_service_commission(request={})
    print(response)


def test_get_servers_ip():
    response = db.get_servers_ip()
    print(response)


# test_generate_transaction()
# test_get_transaction("XXXXXXXXXXXXXXXXXXXXX")
# test_get_services()
# test_get_transaction_limits()
# test_get_service_commission()
# test_get_servers_ip()
