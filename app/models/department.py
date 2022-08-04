from app.models import Optional, SQLModel, Field, Relationship
from app.models import CRUDRouter, date, Column, List, Integer


class DepartmentBase(SQLModel):
    name: str
    id_organisation: int = Field(sa_column=Column("id_organisation", Integer, unique=True))
    description: Optional[str]


class Department(DepartmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    employees: List["Employee"] = Relationship(back_populates="department")


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: int


class DepartmentUpdate(SQLModel):
    description: Optional[str] = None


class DepartmentReadWithEmployees(DepartmentRead):
    team: Optional[DepartmentRead] = None
