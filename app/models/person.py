from app.models import Optional, SQLModel, Field, Relationship
from app.models import date
from app.models import CRUDRouter

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


class PersonRead(PersonBase):
    id: int


class PersonUpdate(SQLModel):
    address: Optional[str] = None


class PersonReadWithEmployee(PersonRead):
    employee: Optional[PersonRead] = None