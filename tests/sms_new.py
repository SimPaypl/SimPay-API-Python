from simpay import Client

apiKey = ""
apiPassword = ""
client = Client(apiKey, apiPassword)
hash = 'MhHCeKSDWNc32LXR'
# print(client.SMS.verify_code(3574, '384AA4').data)
# print(client.SMS.get_service('7886f5b3'))
# print(client.SMS.get_services())
# print(client.SMS.get_transaction(3574, 2276879))
# print(client.SMS.get_transaction('ccbc4b7a', 2276879))
# print(client.SMS.get_services())
# print(client.DirectBilling.generate_transaction('c7d8b925', hash, 1))

print(client.DirectBilling.generate_transaction('c7d8b925', hash, 10))
print(client.DirectBilling.verify_transaction({
  "id": "82493ac0-253a-4c4b-bc1e-0578e0352fed",
  "service_id": "c7d8b925",
  "status": "transaction_db_confirmed",
  "values": {
    "net": 1,
    "gross": 1.23,
    "partner": 0.67
  },
  "number_from": 48440200126,
  "provider": 1,
  "signature": "f554829dd3282fd9239dd28b6e253e900edbac89f5303115286d94d1f8ebe242"
}, hash))