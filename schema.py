from abc import ABC
from typing import Optional

import pydantic


class AbstractProduct(pydantic.BaseModel, ABC):
    header: str
    description: str
    owner: str


class CreateProduct(AbstractProduct):
    header: str
    description: str
    owner: str


class UpdateProduct(AbstractProduct):
    header: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
