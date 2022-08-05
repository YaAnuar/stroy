from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException
from app.models.department import Department, DepartmentCreate, DepartmentUpdate


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


@router.post("/departments")
async def add_department(department: DepartmentCreate, session: AsyncSession = Depends(get_session)):
    res = Department(name=department.name, 
                    id_organisation=department.id_organisation, 
                    description=department.description) 
    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res


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
