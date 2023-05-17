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
    tmobile: bool
    orange: bool
    play: bool
    plus: bool

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_MaxValues(BaseModel):
    tmobile: str
    orange: str
    play: str
    plus: str

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_Commission(BaseModel):
    commission_0: str
    commission_9: str
    commission_25: str


class DCB_Service_Commissions(BaseModel):
    tmobile: DCB_Service_Commission
    orange: DCB_Service_Commission
    play: DCB_Service_Commission
    plus: DCB_Service_Commission

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_Values(BaseModel):
    net: float
    gross: float
    partner: float | None


class DCB_Service_CalculatedCommissions(BaseModel):
    tmobile: DCB_Service_Values | None
    orange: DCB_Service_Values | None
    play: DCB_Service_Values | None
    plus: DCB_Service_Values | None

    class Config:
        fields = {'tmobile': 't-mobile'}
        allow_population_by_field_name = True


class DCB_Service_API(BaseModel):
    complete: str
    failure: str


class DCB_Service(BaseModel):
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
    is_send: bool
    last_send_at: datetime
    count: int


class DCB_Transaction_Returns(BaseModel):
    complete: str
    failure: str


class DCB_Transaction(BaseModel):
    id: str
    status: DCB_Transaction_Status
    phoneNumber: str | None
    control: str | None
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
    transactionId: str
    redirectUrl: str
