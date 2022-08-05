from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException, ValidationError
from app.models.department import Department, DepartmentCreate, DepartmentUpdate, Department_validate


router = APIRouter(
    prefix="/api",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/departments", response_model=list[Department])
async def get_list_departments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).options(selectinload('*')))
    departments = result.scalars().all()

    return departments


@router.get("/department_by_id/{id}", response_model=list[Department])
async def get_department_by_id(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).where(Department.id == id).options(selectinload('*')))
    departments = result.scalars().all()

    return departments


@router.post("/departments/")
async def add_employee(request: Request, session: AsyncSession = Depends(get_session)):
    req = await request.json()
    try:
        Department_validate(req)
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

@router.patch("/departments/{dep_id}")
async def update_department(empl_id: int, employee: DepartmentUpdate, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    req = await request.json()
    exists = await session.execute(select(Department).where(Department.id == empl_id))
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        res = await session.execute("UPDATE department SET description = '{0}' WHERE id = {1} CASCADE"
                                                    .format(req['description'], empl_id))
        await session.commit()
        return 'OK'


@router.delete("/departments/{dep_id}")
async def delete_department(dep_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute("DELETE FROM department where id = {}".format(dep_id))
    await session.commit()
    return 'OK'
