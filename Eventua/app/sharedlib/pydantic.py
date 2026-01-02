import pydantic
from pydantic import BaseModel, Field, field_validator, EmailStr, TypeAdapter
from typing import Optional, List, Dict, Any



class UserDetail(BaseModel):
    fullname: str
    phone: str
    usertype: str
    dob: Optional[str] = None
    email: EmailStr
    password: str

    @field_validator("phone")
    def validate_phone(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return v
    
    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator("username", mode="before")
    def validate_username(cls, v: str) -> str:
        email_adapter = TypeAdapter(EmailStr)
        try:
            v = v.strip()
            if v.isdigit() and len(v) == 10:
                return v
            else:
                email = email_adapter.validate_python(v)
                return email.lower()  # EmailStr already validated
        except Exception:
            raise ValueError("Username must be a valid email or 10-digit phone number")

class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None


class Property(BaseModel):
    key: Optional[str] = None 
    value: Optional[str] = None 
    sort_order: Optional[int] = None

class Node(BaseModel):
    id: Optional[str] = None 
    label: Optional[str] = None 
    sort_order: Optional[int] = None 
    properties: List[Property] = Field(default_factory=list) 
    children: List["Node"] = Field(default_factory=list)


class EventStructure(BaseModel):
    eventName: str
    eventYear: Optional[int] = None 
    eventCountry: Optional[str] = None 
    eventArea: Optional[str] = None 
    eventAreaPin: Optional[int] = None 
    eventStruct: Optional[List[Node]] = None 
    storageType: Optional[str] = None 
    storageKey: Optional[str] = None
    
    @field_validator("eventYear", "eventAreaPin", mode="before") 
    def empty_str_to_none(cls, v): 
        if v == "": 
            return None 
        return v
    
# Resolve forward references for recursive model
Node.model_rebuild()


### Below are all junks or reference for now 
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