import requests


class SMS:
    def __init__(self, api_key, secret, service_id=None):
        self.api_key = api_key
        self.secret = secret
        self.service_id = service_id

    # https://docs.simpay.pl/#weryfikacja-kodu
    def verify_code(self, request):
        if request.get("key") is None:
            request["key"] = self.api_key

        if request.get("secret") is None:
            request["secret"] = self.secret

        if request.get("service_id") is None:
            request["service_id"] = self.service_id

        r = requests.post(SMS.VERIFY_CODE_URL, json={"params": request})

        return r.json()

    # https://docs.simpay.pl/#pobieranie-listy-uslug
    def get_service_list(self, request):
        if request.get("key") is None:
            request["key"] = self.api_key

        if request.get("secret") is None:
            request["secret"] = self.secret

        r = requests.post(SMS.SERVICE_LIST_URL, json={"params": request})

        return r.json()


SMS.VERIFY_CODE_URL = "https://simpay.pl/api/status"
SMS.SERVICE_LIST_URL = "https://simpay.pl/api/get_services"
