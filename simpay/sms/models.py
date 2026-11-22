from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


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
    description: str | None = None
    adult: bool = False
    numbers: list[int] | None = None
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
    from_number: int = Field(alias='from')
    code: str
    used: bool
    send_at: datetime

    model_config = ConfigDict(populate_by_name=True)


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


class SMS_Code(BaseModel):
    """Result of SMS code verification

    :param used: bool
        Whether the code had already been used before this verification
    :param code: str
        SMS code
    :param test: bool
        Whether the code comes from a test SMS
    :param from_number: str
        Phone number the SMS was sent from, origin from api it's 'from'
    :param number: int
        Premium number the SMS was sent to
    :param value: float
        Net value of the number
    :param used_at: datetime | None
        When the code was used, only for codes that had already been used
    """
    used: bool
    code: str
    test: bool
    from_number: str = Field(alias='from')
    number: int
    value: float
    used_at: datetime | None = None

    model_config = ConfigDict(populate_by_name=True)
