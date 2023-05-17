import hashlib
import random
import string
import unicodedata
from simpay.sms_xml.models import PARAMS 


class SMS_XML:
    def __init__(self, api_key):
        self.api_key = api_key

    def check_parameters(self, request):
        for param in PARAMS:
            if request.get(param) is None:
                return False

        return request.get("sign") is not None and request.get("sign") == self.sign(request)

    def generate_code():
        key = ''

        for i in range(6):
            key += random.choice(string.ascii_uppercase + string.digits)

        return key

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
