from payments.sms import SMS

sms = SMS("XXXXXXXXXXXXX", "XXXXXXXXXXXXXXXX", "XXXXXXXXXXXXX")


def test_verify_code():
    response = sms.verify_code(request={"code": "XXXXXXX"})
    print(response)


def test_get_service_list():
    response = sms.get_service_list(request={})
    print(response)


test_verify_code()
test_get_service_list()
