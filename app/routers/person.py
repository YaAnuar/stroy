from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter, HTTPException
from app.models.person import Person, PersonCreate, PersonUpdate

router = APIRouter(
    prefix="/api",
    tags=["persons"],
    responses={404: {"description": "Not found"}},
)

@router.get("/persons", response_model=list[Person])
async def get_persons(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Person))
    persons = result.scalars().all()

    return persons


@router.post("/persons")
async def add_person(person: PersonCreate, session: AsyncSession = Depends(get_session)):
    res = Person(first_name=person.first_name, 
                    last_name=person.last_name, 
                    birthday=person.birthday,
                    address=person.address) 
    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res


@router.patch("/persons/{person_id}", status_code=200)
async def update_person(person_id: int, person: PersonUpdate, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    req = await request.json()
    exists = await session.execute(select(Person).where(Person.id == person_id))
    if not exists:
        raise HTTPException(status_code=404, detail="Person not found")
    else:
        res = await session.execute("UPDATE person SET address = '{0}' WHERE id = {1}"
                                                    .format(req['address'], person_id))
        await session.commit()
        return 'OK'


@router.delete("/persons/{person_id}")
async def delete_employee(person_id: int, session: AsyncSession = Depends(get_session)):
    await session.execute("DELETE FROM person where id = {}".format(person_id))
    await session.commit()
    return 'OK'