from app.models import Optional, SQLModel, Field, Relationship
from app.models import date

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
