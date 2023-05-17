from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class SMS_Service_Status(Enum):
    NEW = 'service_new'
    ACTIVE = 'service_active'
    BLOCKED = 'service_blocked'
    DELETED = 'service_deleted'
    SECOND_VERIFY = 'service_second_verify'
    REJECTED = 'service_rejected'
    VERIFY = 'service_verify'
    ONGOING_REGISTRATION = 'service_ongoing_registration'


class SMS_Service_Type(Enum):
    ONE_TIME_CODE = 'ONE_TIME_CODE'
    CODE_PACK = 'CODE_PACK'
    API_URL = 'API_URL'


class SMS_Service(BaseModel):
    id: str
    type: SMS_Service_Type
    status: SMS_Service_Status
    name: str
    prefix: str
    suffix: str
    description: str | None
    adult: bool = False
    numbers: list[int] | None
    created_at: datetime


class SMS_Transaction(BaseModel):
    id: str
    from_number: int
    code: str
    used: bool
    send_at: datetime

    class Config:
        fields = {'from_number': 'from'}
        allow_population_by_field_name = True


class SMS_Number(BaseModel):
    number: int
    value: float
    value_gross: float
    adult: bool
