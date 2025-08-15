from pydantic import BaseModel
from pydantic import EmailStr, Field, AliasChoices
from pydantic import field_validator, model_validator


from datetime import date
from uuid import UUID, uuid4
from enum import Enum


class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"
    ENGINEERING = "ENGINEERING"

class Employee(BaseModel):
    employee_id: UUID = Field(default_factory=uuid4, frozen=True)
    name: str = Field(min_length=1, frozen=True)
    email: EmailStr = Field(pattern=r".com$")
    date_of_birth: date = Field(alias= AliasChoices('date_of_birth', 'birth_date'), repr=False, frozen=True)
    salary: float = Field(alias=AliasChoices('salary','compensation'), gt=0, repr=False)
    department: Department
    elected_benefits: bool

    @field_validator("date_of_birth")
    @classmethod
    def check_valid_age(cls, date_of_birth: date) -> date:
        today = date.today()
        eighteen_years_ago = date(today.year - 18, today.month, today.day)

        if date_of_birth > eighteen_years_ago:
            raise ValueError("Employees must be at least 18 years old.")

        return date_of_birth

    @model_validator(mode="after")
    def check_it_benefits(self):
        department = self.department
        elected_benefits = self.elected_benefits

        if self.department == 'IT' and elected_benefits:
            raise ValueError(
                "IT employees are contractors and don't qualify for benefits"
            )
        return self


e1 = Employee(
    name="Chris DeTuma",
    email="cdetuma@example.com",
    date_of_birth="1998-04-02",
    salary=123_000.00,
    department="IT",
    elected_benefits=True,
)

print(f'e1\n:{e1}')

new_employee_dict = {
    "name": "Chris DeTuma",
    "email": "mail2mamud@gmail.com",
    "date_of_birth": "1998-04-02",
    "compensation": 123_000.00,
    "department": "HR",
    "elected_benefits": False,
    }

e2 = Employee.model_validate(new_employee_dict)
print(f'e2\n:{e2}')

print(f'e2.model_dump()\n:{e2.model_dump()}')

print(f'e2.model_dump_json()\n:{e2.model_dump_json()}')

print(f'Employee.model_json_schema()\n:{Employee.model_json_schema()}')
