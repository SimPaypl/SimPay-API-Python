from simpay import Client, ClientException

apiKey = ""
apiPassword = ""
hashSign = ""
client = Client(apiKey, apiPassword)

serviceID = "0d742940"
smsService = client.DirectBilling.get_service(serviceID)
smsServiceTransactions = client.DirectBilling.get_transactions(serviceID)

try:
    transaction = client.DirectBilling.generate_transaction(serviceID, hashSign, 1)
    # Redirect customer to url from variable transaction.redirectUrl
    # Optional validation BY specific number, client.SMS.verify_code(serviceID, 'CODE', NUMBER)
    verified = client.DirectBilling.verify_transaction("...POST FIELDS from http as dict", hashSign)
except ClientException as error:
    print(error.message)