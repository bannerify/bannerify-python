"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from bannerify import utils
from bannerify.types import BaseModel
from enum import Enum
import pydantic
from typing import TypedDict
from typing_extensions import Annotated


class ErrConflictCode(str, Enum):
    r"""A machine readable error code."""
    CONFLICT = "CONFLICT"

class ErrConflictErrorTypedDict(TypedDict):
    code: ErrConflictCode
    r"""A machine readable error code."""
    docs: str
    r"""A link to our documentation with more details about this error code"""
    message: str
    r"""A human readable explanation of what went wrong"""
    request_id: str
    r"""Please always include the requestId in your error report"""
    

class ErrConflictError(BaseModel):
    code: ErrConflictCode
    r"""A machine readable error code."""
    docs: str
    r"""A link to our documentation with more details about this error code"""
    message: str
    r"""A human readable explanation of what went wrong"""
    request_id: Annotated[str, pydantic.Field(alias="requestId")]
    r"""Please always include the requestId in your error report"""
    
class ErrConflictData(BaseModel):
    error: ErrConflictError
    


class ErrConflict(Exception):
    r"""This response is sent when a request conflicts with the current state of the server."""
    data: ErrConflictData

    def __init__(self, data: ErrConflictData):
        self.data = data

    def __str__(self) -> str:
        return utils.marshal_json(self.data, ErrConflictData)

