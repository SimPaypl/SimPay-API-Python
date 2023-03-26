from payments.sms import SMS

sms = SMS(api_key='0b4dca15', api_password='3eea38f407073ff0abff956b57d71783')


# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-listy-uslug
print( sms.get_service_list() )
print( sms.get_service_list_paginated(page=1, limit=100) )

# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-informacji-o-usludze
print( sms.get_service(service_id=3549) )

# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-listy-transakcji
print( sms.get_transaction_list(service_id=3549) )
print( sms.get_transaction_list_paginated(service_id=3549, page=1, limit=100) )

# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-informacji-o-transakcji
print( sms.get_transaction(service_id=3549, transaction_id=2216609) )

# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-dostepnych-numerow-dla-uslugi
print( sms.get_service_numbers(service_id=3549) )
print( sms.get_service_numbers_paginated(service_id=3549, page=1, limit=100) )

# https://docs.simpay.pl/pl/python/?python#sms-informacji-o-pojedynczym-numerze-uslugi
print( sms.get_service_number(service_id=3549, number=7055) )

# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-wszystkich-dostepnych-numerow
print( sms.get_numbers() )
print( sms.get_numbers_paginated(page=1, limit=100) )

# https://docs.simpay.pl/pl/python/?python#sms-pobieranie-pojedynczego-numeru-sms
print( sms.get_number(number=7055) )

# https://docs.simpay.pl/pl/python/?python#sms-weryfikacja-poprawnosci-kodu
print( sms.verify_sms_code(service_id=3549, code='81FFC5', number=7055) )
print( sms.verify_sms_code(service_id=3549, code='81FFC5') )
