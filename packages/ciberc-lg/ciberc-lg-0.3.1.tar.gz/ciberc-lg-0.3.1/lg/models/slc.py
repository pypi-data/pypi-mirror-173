from pydantic import BaseModel, Field
from typing import List, Optional


class StatusParameters(BaseModel):
    date_time_field: str = Field(alias='datetimefield')
    lamp_status: str = Field(alias='lamp Status')
    voltage_under_over: str = Field(alias='voltage Under Over')
    lamp: str
    communication: str
    driver: str


class PowerParameters(BaseModel):
    tilt: Optional[float]
    voltage: float
    current: float
    watts: float
    cumulative_kilowatt_hrs: float = Field(alias='cumulative KiloWatt Hrs')
    burn_hrs: float = Field(alias='burn Hrs')
    dimming: float
    power_factor: float = Field(alias='power Factor')
    mode: str


class SLCData(BaseModel):
    slc_no: int
    status_parameters: StatusParameters
    power_parameters: PowerParameters


class SLCBase(BaseModel):
    page_no: int = Field(..., alias='pageno')
    page_size: int = Field(..., alias='pagesize')
    total_page_count: int = Field(..., alias='totalpagecount')


class SLCDataList(SLCBase):
    slc_data_list: List[SLCData] = Field(alias='slcDataList')


class SLCDataResponse(BaseModel):
    data: SLCDataList
    status: str


# ---


class SLC(BaseModel):
    serial_number: int
    slc_name: str
    slc_number: int
    address: str
    connected_since: str  # 2021-12-09 21:37:30.000
    created_on: str = Field(..., alias='createdon')  # 2021-12-09T20:07:48.557
    current_lamp_status: str
    gateway_name: str = Field(alias='gatewayname')
    ip_address: Optional[str] = Field(alias='ipAddress')
    latitude: float
    longitude: float
    uid: str
    slc_group: str = None


class SLCList(SLCBase):
    all_slcs_list: List[SLC] = Field(..., alias='allslcslist')


class SLCResponse(BaseModel):
    data: SLCList
    status: int


# ---


class SLCInfo(SLCData, SLC):
    """No related directly with server response, instead join to models.

    Join differents LG SLC Models:

    - SLC Model
    - SLCData Model

    In order to generate a complete list of attributes incluiding:
    Latitud, Longitude

    Use:

    .. code-block:

        SLCInfo(
            **{
                **slc.dict(by_alias=True),
                **slc_data.dict(by_alias=True)
            }
        )
    """
