"""Pydantic Models for Cincom LG"""

from .gateway import GatewayResponse
from .slc import (
    SLCDataResponse,
    SLCInfo,
    SLCResponse
)
from .switch import SwitchOnOffResponse

__all__ = [
    "GatewayResponse",
    "SLCDataResponse",
    "SLCInfo",
    "SLCResponse",
    "SwitchOnOffResponse",
]
