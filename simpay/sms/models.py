from __future__ import annotations
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
    """SMS service model

    :param id: str
        ID of service, short UUID
    :param type: SMS_Service_Type
        Type of service
    :param name: str
        Name of service
    :param prefix: str
        Prefix of SMS
    :param description: str | None
        Description of service
    :param adult: bool
        Service it's for adult content age, default it's false
    :param numbers: list[int] | none
        List of available numbers for this service
    :param created_at: datetime
        Created at
    """
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
    """SMS transaction model

    :param id: str
        ID of SMS transaction, short UUID
    :param from_number: int
        Origin number of sender, origin from api it's 'from'
    :param code: str
        SMS code
    :param used: bool
        Determinate if code has been used
    :param send_at: datetime
        Sended at
    """
    id: str
    from_number: int
    code: str
    used: bool
    send_at: datetime

    class Config:
        fields = {'from_number': 'from'}
        allow_population_by_field_name = True


class SMS_Number(BaseModel):
    """SMS number model

    :param number: int
        Number of SMS
    :param value: float
        Net value
    :param value_gross: float
        Gross value
    :param adult: bool
        Determinate if number it's for adult content age
    """
    number: int
    value: float
    value_gross: float
    adult: bool
