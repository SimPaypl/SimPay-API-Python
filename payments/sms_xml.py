import hashlib
import random
import string
import unicodedata

import requests


class SMS_XML:
    def __init__(self, api_key):
        self.api_key = api_key

    # https://docs.simpay.pl/#odbieranie-informacji-o-sms
    def check_parameters(self, request):
        for param in SMS_XML.PARAMS:
            if request.get(param) is None:
                return False

        return request.get("sign") is not None and request.get("sign") == self.sign(request)

    # https://docs.simpay.pl/#odbieranie-informacji-o-sms
    @staticmethod
    def generate_code():
        key = ''

        for i in range(6):
            key += random.choice(string.ascii_uppercase + string.digits)

        return key

    # https://docs.simpay.pl/#lista-ip-serwerow-simpay
    @staticmethod
    def get_servers_ip():
        r = requests.get(SMS_XML.GET_IP_URL)

        return r.json()

    # https://docs.simpay.pl/#odbieranie-informacji-o-sms
    @staticmethod
    def generate_xml(code):
        header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><sms-response>"
        footer = "<sms-text></sms-text></sms-response>"

        return header + unicodedata.normalize(code, "NKFD") + footer

    def sign(self, request):
        return hashlib.new('sha256',
                           bytes(
                               str(request.get("sms_id")) +
                               str(request.get("sms_text")) +
                               str(request.get("sms_from")) +
                               str(request.get("send_number")) +
                               str(request.get("send_time")) +
                               str(self.api_key),
                               encoding="utf8")
                           ).hexdigest()


SMS_XML.GET_IP_URL = "https://simpay.pl/api/get_ip"
SMS_XML.CODES = {
    "7055": 0.25,
    "7136": 0.5,
    "7255": 1.0,
    "7355": 1.5,
    "7455": 2.0,
    "7555": 2.5,
    "7636": 3.0,
    "77464": 3.5,
    "78464": 4.0,
    "7936": 4.5,
    "91055": 5.0,
    "91155": 5.5,
    "91455": 7.0,
    "91664": 8.0,
    "91955": 9.5,
    "92055": 10.0,
    "92555": 12.5
}
SMS_XML.PARAMS = ["send_number", "sms_text", "sms_from", "sms_id", "sign"]
