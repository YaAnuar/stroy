from app.models import Optional, SQLModel, Field, Relationship
from app.models import date, List
from app.models import CRUDRouter
from app.models.department import Department
from app.models.person import Person


class EmployeeBase(SQLModel):
    tab: int
    hire_date: Optional[date]
    dismissal_date: Optional[date]


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    id_person: Optional[int] = Field(default=None, foreign_key="person.id")
    id_department: Optional[int] = Field(default=None, foreign_key="department.id")
    person: Optional[Person] = Relationship(back_populates="employee")
    department: Optional[Department] = Relationship(back_populates="employees")


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(SQLModel):
    tab: Optional[int] = None
    hire_date: Optional[date]
    dismissal_date: Optional[date]


class EmployeeReadWithPersonandDepartment(EmployeeRead):
    department: Optional[Department] = None
    person: Optional[Person] = None
