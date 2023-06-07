from simpay import Client, ClientException

apiKey = ""
apiPassword = ""
client = Client(apiKey, apiPassword)

serviceID = "0d742940"
smsService = client.SMS.get_service(serviceID)
smsServiceTransactions = client.SMS.get_transactions(serviceID)

try:
    transaction = client.SMS.verify_code(serviceID, 'CODE')
    # Optional validation by specific number, client.SMS.verify_code(serviceID, 'CODE', NUMBER)
except ClientException as error:
    print(error.message)