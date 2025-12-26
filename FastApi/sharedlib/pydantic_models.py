from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class user(BaseModel):
    usertype: str
    username: str
    password: str

   

class organization(BaseModel):
    orgName: str = Field(description="This is org name") 
    contactName: str
    
class organizationDisplay(BaseModel):
    orgName: str
    class Config:
        orm_mode = True




    
    class Config:
        json_schema_extra = {
            "example" : {
                "orgName": "Vivekananda Sangha" ,
                "contactName": "Robi Banerjee"
            }
        }

class group(BaseModel):
    groupName: str
    groupDesc: str
    
class event(BaseModel):
    eventName: str
    eventGroups: List[group]
    
class fixture(BaseModel):
    org: organization
    events: List[event]

class participant(BaseModel):
    id: Optional[int] = Field(description = "Id not needed on create", default = None )
    name: str = Field(min_length = 3)
    mobileNo: int
    age: int

    @field_validator("mobileNo")
    def validate_mobile(cls, v):
        if len(str(v)) != 10 or not str(v).isdigit():
            raise ValueError("Mobile number must be exactly 10 digits")
        return v

    @field_validator("age")
    def validate_age(cls, v):
        if not (1 <= v <= 120):
            raise ValueError("Age must be between 1 and 120")
        return v