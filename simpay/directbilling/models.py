from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class DCB_Service_Status(Enum):
    NEW = 'service_db_new'
    ACTIVE = 'service_db_active'
    BLOCKED = 'service_db_rejected'
    DELETED = 'service_db_ongoing_registration'


class DCB_Transaction_Status(Enum):
    NEW = 'transaction_db_new'
    CONFIRMED = 'transaction_db_confirmed'
    REJECTED = 'transaction_db_rejected'
    CANCELED = 'transaction_db_canceled'
    PAYED = 'transaction_db_payed'
    GENERATE_ERROR = 'transaction_db_generate_error'


class DCB_Amount_Type(Enum):
    NET = 'net'
    GROSS = 'gross'
    REQUIRED = 'required'


class DCB_Provider(Enum):
    ORANGE = 1
    PLUS = 2
    PLAY = 3
    TMOBILE = 4


class DCB_Service_Providers(BaseModel):
    """DCB service available providers

    :param tmobile: bool
        Provider t-mobile available status, origin key from api's it's 't-mobile'
    :param orange: bool
        Type of service
    :param play: bool
        Name of service
    :param plus: bool
        Prefix of SMS
    """
    tmobile: bool
    orange: bool
    play: bool
    plus: bool

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_MaxValues(BaseModel):
    """DCB service max values per single transaction

    :param tmobile: str
        Value for t-mobile provider, origin key from api's it's 't-mobile'
    :param orange: str
        Value for orange provider
    :param play: str
        Value for orange provider
    :param plus: str
        Value for orange provider
    """
    tmobile: str
    orange: str
    play: str
    plus: str

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_Commission(BaseModel):
    """DCB servicem stages of comission rates

    :param commission_0: str
        Commision rate from 0,01 PLN to 9,99 PLN amount of transaction
    :param commission_9: str
        Commision rate from 9 PLN to 24,99 PLN amount of transaction
    :param commission_25: str
        Commision rate from 25 PLN to max amount of transaction
    """
    commission_0: str
    commission_9: str
    commission_25: str


class DCB_Service_Commissions(BaseModel):
    """DCB service comission rates

    :param tmobile: DCB_Service_Commission
        Commision rate for t-mobile provider, origin key from api's it's 't-mobile'
    :param orange: DCB_Service_Commission
        Commision rate for orange provider
    :param play: DCB_Service_Commission
        Commision rate for play provider
    :param plus: DCB_Service_Commission
        Commision rate for plus provider
    """
    tmobile: DCB_Service_Commission
    orange: DCB_Service_Commission
    play: DCB_Service_Commission
    plus: DCB_Service_Commission

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_Values(BaseModel):
    """DCB service and transaction values

    :param net: float
        Amount net
    :param gross: float
        Amount gross
    :param partner: float | None
        Partner comission amount from transaction
    """
    net: float
    gross: float
    partner: float | None


class DCB_Service_CalculatedCommissions(BaseModel):
    """DCB service calculated comissions

    :param tmobile: DCB_Service_Values | None
        Values for t-mobile provider, origin key from api's it's 't-mobile'
    :param orange: DCB_Service_Values | None
        Values for orange provider
    :param play: DCB_Service_Values | None
        Values for play provider
    :param plus: DCB_Service_Values | None
        Values for plus provider
    """
    tmobile: DCB_Service_Values | None
    orange: DCB_Service_Values | None
    play: DCB_Service_Values | None
    plus: DCB_Service_Values | None

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_API(BaseModel):
    """DCB service redirection urls

    :param complete: str
        Redirection url after complete transaction
    :param failure: str
        Redirection url after failure transaction
    """
    complete: str
    failure: str


class DCB_Service(BaseModel):
    """DCB service

    :param id: str
        ID of DirectBilling service
    :param name: str
        Name of DirectBilling service
    :param suffix: str
        Suffix
    :param status: DCB_Service_Status
        Status
    :param api: DCB_Service_API
        API endpoints
    :param providers: DCB_Service_Providers
        Available providers
    :param commissions: DCB_Service_Commissions
        Commisions
    :param maxValues: DCB_Service_MaxValues
        Max values per transaction
    :param created_at: datetime
        Creation time of service
    """
    id: str
    name: str
    suffix: str
    status: DCB_Service_Status
    api: DCB_Service_API
    providers: DCB_Service_Providers
    commissions: DCB_Service_Commissions
    maxValues: DCB_Service_MaxValues
    created_at: datetime


class DCB_Transaction_Notify(BaseModel):
    """DCB transaction notification states

    :param is_send: str
        Status whether notification has been sended
    :param last_send_at: str
        Date of last notification attempt
    :param count: str
        Count of notification attemps
    """
    is_send: bool
    last_send_at: datetime
    count: int


class DCB_Transaction_Returns(BaseModel):
    """DCB transaction redirection urls

    :param complete: str
        URL where customer will be redirected after successful transaction
    :param failure: str
        URL where customer will be redirected after failure transaction
    """
    complete: str
    failure: str


class DCB_Transaction(BaseModel):
    """DCB transaction

    :param id: str
        ID of DirectBilling of transaction
    :param status: DCB_Transaction_Status
        Status
    :param phoneNumber: str | None
        Phone number which transaction has been processed, original key from api it's number_from
    :param control: str | None
        Own custom property
    :param value: float | None
        Amount of transaction
    :param value_netto: float | None
        Amount of transaction (presented as netto value)
    :param operator: str | None
        Operator of transaction
    :param returns: DCB_Transaction_Returns | None
        Returns endpoints after successful or failure transaction
    :param notify: DCB_Transaction_Notify | None
        Nofication statuses
    :param provider: int | None
        ID of transaction provider
    :param signature: str | None
        Signature of transaction based on sha256
    :param created_at: datetime | None
        Creation date of transaction
    :param updated_at: datetime | None
        Update date of transaction
    """
    id: str
    status: DCB_Transaction_Status
    phoneNumber: str | None
    value: float | None
    value_netto: float | None
    values: DCB_Service_Values | None
    operator: str | None
    returns: DCB_Transaction_Returns | None
    notify: DCB_Transaction_Notify | None
    control: str | None
    provider: int | None
    signature: str | None
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        fields = {'phoneNumber': 'number_from'}
        allow_population_by_field_name = True


class DCB_GeneratedTransaction(BaseModel):
    """DCB generating transaction callback

    :param transactionId: str
        Transaction ID
    :param redirectUrl: str
        Redirection url for transaction
    """
    transactionId: str
    redirectUrl: str
