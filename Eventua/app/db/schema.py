from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class loginProfile(BaseModel):
    username: str
    password: str

