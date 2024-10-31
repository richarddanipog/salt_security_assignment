from pydantic import BaseModel
from typing import List, Union

class Parameter(BaseModel):
    name: str
    types: List[str]
    required: bool

class APIModel(BaseModel):
    path: str
    method: str
    query_params: List[Parameter] = []
    headers: List[Parameter] = []
    body: List[Parameter] = []

class RequestParameter(BaseModel):
    name: str
    value: Union[str, int, bool, List[Union[str, int, dict]]]

class RequestData(BaseModel):
    path: str
    method: str
    query_params: List[RequestParameter] = []
    headers: List[RequestParameter] = []
    body: List[RequestParameter] = []
