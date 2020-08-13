import decimal
import hashlib
import requests


class DirectBilling:
    def __init__(self, api_key, secret, debug_mode=False, service_id=None):
        self.api_key = api_key
        self.secret = secret
        self.debug_mode = debug_mode
        self.service_id = service_id

    @staticmethod
    def format_number(num):
        try:
            dec = decimal.Decimal(num)
        except[]:
            return "BAD_FORMAT"
        tup = dec.as_tuple()
        delta = len(tup.digits) + tup.exponent
        digits = ''.join(str(d) for d in tup.digits)
        if delta <= 0:
            zeros = abs(tup.exponent) - len(tup.digits)
            val = '0.' + ('0' * zeros) + digits
        else:
            val = digits[:delta] + ('0' * tup.exponent) + '.' + digits[delta:]
        val = val.rstrip('0')
        if val[-1] == '.':
            val = val[:-1]
        if tup.sign:
            return '-' + val
        return val

    # https://docs.simpay.pl/#generowanie-transakcji
    def generate_transaction(self, api_key, request):
        if request.get("serviceId") is None:
            request["serviceId"] = self.service_id

        amount = ""

        if request.get("amount") is not None:
            amount = request["amount"]

        if request.get("amount_gross") is not None:
            amount = request["amount_gross"]

        if request.get("amount_required") is not None:
            amount = request["amount_required"]

        amount = self.format_number(amount)

        request["sign"] = hashlib.new('sha256',
                                      bytes(
                                          str(request["serviceId"]) +
                                          str(amount) +
                                          str(request.get("control")) +
                                          str(api_key),
                                          encoding="utf8")
                                      ).hexdigest()

        r = requests.post(DirectBilling.API_URL, data=request)

        return r.json()

    # https://docs.simpay.pl/#pobieranie-danych-o-transakcji
    def get_transaction(self, request):
        if request.get("key") is None:
            request["key"] = self.api_key

        if request.get("secret") is None:
            request["secret"] = self.secret

        print(request)

        r = requests.post(DirectBilling.TRANSACTION_STATUS_URL, json={"params": request})

        return r.json()

    # https://docs.simpay.pl/#pobieranie-listy-uslug-dcb
    def get_services(self, request):
        if request.get("key") is None:
            request["key"] = self.api_key

        if request.get("secret") is None:
            request["secret"] = self.secret

        r = requests.post(DirectBilling.SERVICES_LIST_URL, json={"params": request})

        return r.json()

    # https://docs.simpay.pl/#pobieranie-maksymalnych-kwot-transakcji
    def get_transaction_limits(self, request):
        if request.get("key") is None:
            request["key"] = self.api_key

        if request.get("secret") is None:
            request["secret"] = self.secret

        if request.get("service_id") is None:
            request["service_id"] = self.service_id

        r = requests.post(DirectBilling.TRANSACTION_LIMITS_URL, json={"params": request})

        return r.json()

    # https://docs.simpay.pl/#pobieranie-prowizji-dla-uslugi
    def get_service_commission(self, request):
        if request.get("key") is None:
            request["key"] = self.api_key

        if request.get("secret") is None:
            request["secret"] = self.secret

        if request.get("service_id") is None:
            request["service_id"] = self.service_id

        r = requests.post(DirectBilling.SERVICE_COMMISSION_URL, json={"params": request})

        return r.json()

    # https://docs.simpay.pl/#lista-ip-serwerow-simpay
    @staticmethod
    def get_servers_ip():
        r = requests.get(DirectBilling.GET_IP_URL)

        return r.json()

    # https://docs.simpay.pl/#odbieranie-transakcji
    def sign(self, id, status, valuenet, valuepartner, control):
        return hashlib.new('sha256',
                           bytes(
                               str(id) +
                               str(status) +
                               str(valuenet) +
                               str(valuepartner) +
                               str(control) +
                               str(self.api_key),
                               encoding="utf8")
                           ).hexdigest()


DirectBilling.API_URL = "https://simpay.pl/db/api"
DirectBilling.TRANSACTION_STATUS_URL = "https://simpay.pl/api/db_status"
DirectBilling.SERVICES_LIST_URL = "https://simpay.pl/api/get_services_db"
DirectBilling.TRANSACTION_LIMITS_URL = "https://simpay.pl/api/db_hosts"
DirectBilling.SERVICE_COMMISSION_URL = "https://simpay.pl/api/db_hosts_commission"
DirectBilling.GET_IP_URL = "https://simpay.pl/api/get_ip"
