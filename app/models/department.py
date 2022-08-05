from app.models import Optional, SQLModel, Field, Relationship
from app.models import Column, List, Integer


def Department_validate(req):
    return DepartmentBase.validate({"first_name": req['name'], "last_name": req['id_organisation'], 
                                    "description": req['description']})


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
    id_organisation: int = None
    description: Optional[str] = None
