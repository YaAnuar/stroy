from wsgiref import validate
from app.models import Optional, SQLModel, Field, Relationship
from app.models import Column, List, Integer
from pydantic import validator


class DepartmentBase(SQLModel):
    name: str
    id_organisation: int = Field(sa_column=Column("id_organisation", Integer, unique=True))
    description: Optional[str]


class Department(DepartmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    employees: List["Employee"] = Relationship(back_populates="department")


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(SQLModel):
    name: str = None
    id_organisation: Optional[int] = None
    description: Optional[str] = None
