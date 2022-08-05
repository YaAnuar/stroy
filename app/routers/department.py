from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException, ValidationError
from app.models.department import Department, DepartmentCreate, DepartmentUpdate, Department_validate


router = APIRouter(
    prefix="/api",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_list_departments", response_model=list[Department])
async def get_list_departments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).options(selectinload('*')))
    departments = result.scalars().all()

    return departments


@router.get("/get_department_by_id/{id}", response_model=list[Department])
async def get_department_by_id(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).where(Department.id == id).options(selectinload('*')))
    departments = result.scalars().all()

    return departments


@router.post("/add_department/")
async def add_department(request: Request, session: AsyncSession = Depends(get_session)):
    req = await request.json()
    try:
        if {'name', 'id_organisation', 'description'} <= set(req):
            Department_validate(req)
        else:
            return  HTTPException(status_code=400, detail="Missed request value.")
    except ValidationError as e:
        return  HTTPException(status_code=400, detail="Incorrect values: " + str(e))
    else:
        dep = Department(tab=req['name'], 
                        id_person=req['id_organisation'], 
                        id_department=req['description'])
        session.add(dep)
        await session.commit()
        await session.refresh(dep)

        return dep

@router.patch("/update_department/{dep_id}")
async def update_department(dep_id: int, employee: DepartmentUpdate, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    req = await request.json()
    res = await session.execute(select(Department).where(Department.id == dep_id))
    exists = res.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        try:
            if {'name', 'id_organisation', 'description'} <= set(req):
                Department_validate(req)
            else:
                return  HTTPException(status_code=400, detail="Missed request value.")
        except ValidationError as e:
            return  HTTPException(status_code=400, detail="Incorrect values:")
        else:
            await session.execute("UPDATE department SET first_name = '{0}', last_name = '{1}', "
                                                        "id_organisation = '{2}', description = '{3}'  WHERE id = {4}"
                                                        .format(req['first_name'], req['last_name'], req['id_organisation'], 
                                                        req['description'], dep_id))
            await session.commit()
            return 'OK'


@router.delete("/delete_department/{dep_id}")
async def delete_department(dep_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute("DELETE FROM department where id = {}".format(dep_id))
    await session.commit()
    return 'OK'
