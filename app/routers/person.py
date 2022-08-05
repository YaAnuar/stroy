from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter, HTTPException
from app.models.person import Person, PersonCreate, PersonUpdate, Person_validate
from app.routers import HTTPException, ValidationError

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


@router.get("/get_person_by_id/{id}", response_model=list[Person])
async def get_person_by_id(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Person).where(Person.id == id))
    persons = result.scalars().all()

    return persons


@router.post("/add_person")
async def add_person(request: Request, session: AsyncSession = Depends(get_session)):
    req = await request.json()
    try:
        Person_validate(req)
    except ValidationError as e:
        return  HTTPException(status_code=400, detail="Incorrect values: " + str(e))
    else:
        pers = Person(first_name=req['first_name'], 
                        last_name=req['last_name'], 
                        birthday=req['birthday'],
                        address=req['address'])
        session.add(pers)
        await session.commit()
        await session.refresh(pers)

        return pers 


@router.patch("/update_person/{person_id}")
async def update_department(person_id: int, person: PersonUpdate, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    req = await request.json()
    res = await session.execute(select(Person).where(Person.id == person_id))
    exists = res.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        try:
            Person_validate(req)
        except ValidationError as e:
            res = await session.execute("UPDATE person SET first_name = '{0}', last_name = '{1}', birthday = '{3}', address = '{4}'  WHERE id = {1} CASCADE"
                                                        .format(req['first_name'], req['last_name'], req['birthday'], req['address'], person_id))
            await session.commit()
            return 'OK'



@router.delete("/delete_person/{person_id}")
async def delete_person(person_id: int, session: AsyncSession = Depends(get_session)):
    await session.execute("DELETE FROM person where id = {}".format(person_id))
    await session.commit()
    return 'OK'