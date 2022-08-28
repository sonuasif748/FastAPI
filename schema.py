from typing import Optional
from pydantic import BaseModel

class AddressBase(BaseModel):
    address: str
    coordinate: str

class AddressAdd(AddressBase):
    id: int

    class Config:
        orm_mode = True


class Addres(AddressAdd):
    id: int

    class Config:
        orm_mode = True


class UpdateAddress(BaseModel):
    address: Optional[str] = None
    coordinate: Optional[str] = None

    class Config:
        orm_mode = True