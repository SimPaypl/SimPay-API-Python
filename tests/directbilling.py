from payments.directbilling import DirectBilling

db = DirectBilling(api_key='0b4dca15', api_password='3eea38f407073ff0abff956b57d71783')


# https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-listy-uslug
print( db.get_service_list() )
print( db.get_service_list_paginated(page=1, limit=100) )

# https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-informacji-o-usludze
print( db.get_service(service_id=158) )

# https://docs.simpay.pl/pl/python/?python#directbilling-kalkulacja-prowizji
print( db.calculate_commission(service_id=158, amount=10.00) )

# https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-listy-transakcji
print( db.get_transaction_list(service_id=158) )
print( db.get_transaction_list_paginated(service_id=158, page=1, limit=100) )

# https://docs.simpay.pl/pl/python/?python#directbilling-pobieranie-informacji-o-transakcji
print( db.get_transaction(service_id=158, transaction_id=1000) )

# https://docs.simpay.pl/pl/python/?python#directbilling-generowanie-transakcji
print( db.create_transaction(service_id=158, key='XXXXXXXX', request={"control": "XXXXXX", "amount": 10.00}) )
