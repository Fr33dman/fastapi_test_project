from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional, List, Union


class Anagrams(BaseModel):
    s1: str
    s2: str


class DeviceTypeField(Enum):
    emeter = 'emeter'
    zigbee = 'zigbee'
    lora = 'lora'
    gsm = 'gsm'


class DeviceModel(BaseModel):
    dev_id: str
    dev_type: DeviceTypeField
    endpoint: Union[str, None]


class DeviceTypeListModel(BaseModel):
    type: DeviceTypeField
    count: int
    devices: List[DeviceModel]


class DevicesModel(BaseModel):
    devices: List[DeviceTypeListModel] = None
