from lib2to3.pgen2.token import NUMBER
import string
from app.models import Optional, SQLModel, Field, Relationship
from app.models import date
from app.models.department import Department
from app.models.person import Person
from pydantic import validator, ValidationError
from sqlalchemy import Integer

def EmployeeBase_validate(req):
    return EmployeeBase.validate({"id_person": req['id_person'], "id_department": req['id_department'], 
                                    "tab": req['tab'], "hire_date": req['hire_date'], "dismissal_date": req['dismissal_date']})


class EmployeeBase(SQLModel):
    id_person: Optional[int] = Field(default=None, foreign_key="person.id")
    id_department: Optional[int] = Field(default=None, foreign_key="department.id")
    tab: int
    hire_date: Optional[date]
    dismissal_date: Optional[date]


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    person: Optional[Person] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="employee")
    department: Optional[Department] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="employees")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeUpdate(SQLModel):
    tab: Optional[int] = None
    hire_date: Optional[date] = None
    dismissal_date: Optional[date] = None
    id_person: Optional[int] = None
    id_department: Optional[int] = None

class EmployeeReadAll(EmployeeRead):
    department: Optional[Department] = None
    person: Optional[Person] = None

