from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter, HTTPException
from app.models.person import Person, PersonCreate, PersonUpdate, Person_validate
from app.routers import HTTPException

router = APIRouter(
    prefix="/api",
    tags=["persons"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_list_persons", response_model=list[Person])
async def get_list_persons(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Person))
    persons = result.scalars().all()

    return persons


@router.get("/get_person_by_id/{id}", response_model=Person)
async def get_person_by_id(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Person).where(Person.id == id))
    person = result.scalars().one()

    return person


@router.post("/create_person", response_model=Person)
async def create_person(person: PersonCreate, session: AsyncSession = Depends(get_session)):
    pers = Person(first_name=person.first_name, 
                    last_name=person.last_name, 
                    birthday=person.birthday,
                    address=person.address)
    session.add(pers)
    await session.commit()
    await session.refresh(pers)

    return pers 


@router.patch("/update_person/{person_id}", response_model=PersonUpdate)
async def update_person_by_id(person_id: int, person: PersonUpdate, session: AsyncSession = Depends(get_session)):
    res = await session.get(Person, person_id)
    if not res:
        raise HTTPException(status_code=404, detail="Person not found")
    else:
        person_data = person.dict(exclude_unset=True)
        for key, value in person_data.items():
            setattr(res, key, value)
        await session.commit()
        return person


@router.delete("/delete_person/{person_id}")
async def delete_person(person_id: int, session: AsyncSession = Depends(get_session)):
    await session.execute("DELETE FROM person where id = {}".format(person_id))
