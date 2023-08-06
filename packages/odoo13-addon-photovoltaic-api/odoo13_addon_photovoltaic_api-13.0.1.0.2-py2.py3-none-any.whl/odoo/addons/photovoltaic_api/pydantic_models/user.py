from .orm_model import OrmModel
from pydantic import EmailStr, Field, validator
from typing import List, Optional
from .info import PersonType, State, Country
from .bank_account import BankAccountOut
class UserShort(OrmModel):
    id:                Optional[int]
    firstname:         Optional[str]
    lastname:          Optional[str]
    vat:               Optional[str]
    gender:            Optional[str] = Field(alias='gender_partner')
    birthday:          Optional[str]
    alias:             Optional[str]

class UserIn(OrmModel):
    person_type:    Optional[int]= Field(alias='person_type_id')
    firstname:      Optional[str]
    lastname:       Optional[str]
    street:         Optional[str]
    street2:        Optional[str] = Field(alias='additional_street')
    zip:            Optional[str]
    city:           Optional[str]
    state_id:       Optional[int]
    country_id:     Optional[int]
    email:          Optional[EmailStr]
    phone:          Optional[str]
    alias:          Optional[str]
    vat:            Optional[str]
    gender_partner: Optional[str] = Field(alias='gender')
    birthday:       Optional[str]
    representative: Optional[UserShort]

class UserOut(OrmModel):
    id:                int
    person_type:       str
    firstname:         str
    lastname:          str
    street:            str
    additional_street: Optional[str]
    zip:               str
    city:              str
    state:             State
    country:           Country
    email:             EmailStr
    phone:             str
    alias:             Optional[str]
    vat:               str
    gender:            Optional[str]
    birthday:          str
    bank_accounts:     List[BankAccountOut]
    representative:    Optional[UserShort]

