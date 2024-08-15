"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from bannerify import utils
from bannerify.types import BaseModel
from enum import Enum
import pydantic
from typing import TypedDict
from typing_extensions import Annotated


class Code(str, Enum):
    r"""A machine readable error code."""
    BAD_REQUEST = "BAD_REQUEST"

class ErrorTypedDict(TypedDict):
    code: Code
    r"""A machine readable error code."""
    docs: str
    r"""A link to our documentation with more details about this error code"""
    message: str
    r"""A human readable explanation of what went wrong"""
    request_id: str
    r"""Please always include the requestId in your error report"""
    

class Error(BaseModel):
    code: Code
    r"""A machine readable error code."""
    docs: str
    r"""A link to our documentation with more details about this error code"""
    message: str
    r"""A human readable explanation of what went wrong"""
    request_id: Annotated[str, pydantic.Field(alias="requestId")]
    r"""Please always include the requestId in your error report"""
    
class ErrBadRequestData(BaseModel):
    error: Error
    


class ErrBadRequest(Exception):
    data: ErrBadRequestData

    def __init__(self, data: ErrBadRequestData):
        self.data = data

    def __str__(self) -> str:
        return utils.marshal_json(self.data, ErrBadRequestData)

