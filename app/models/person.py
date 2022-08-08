from app.models import Optional, SQLModel, Field, Relationship
from app.models import date


def Person_validate(req):
    return PersonBase.validate({"first_name": req['first_name'], "last_name": req['last_name'], 
                                    "birthday": req['birthday'], "address": req['address']})


class PersonBase(SQLModel):
    first_name: str
    last_name: str
    birthday: Optional[date]
    address: str


class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    employee: Optional["Employee"] = Relationship(back_populates="person")


class PersonCreate(PersonBase):
    pass


class PersonUpdate(SQLModel):
    address: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None