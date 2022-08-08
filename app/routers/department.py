from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException
from app.models.department import Department, DepartmentCreate, DepartmentUpdate


router = APIRouter(
    prefix="/api",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_list_departments", response_model=list[Department])
async def get_list_departments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).options(selectinload('*')))
    department = result.scalars().all()

    return department


@router.get("/get_department_by_id/{id}", response_model=Department)
async def get_department_by_id(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).where(Department.id == id).options(selectinload('*')))
    departments = result.scalars().one()

    return departments


@router.post("/create_department/", response_model=Department)
async def create_department(department: DepartmentCreate, session: AsyncSession = Depends(get_session)):
    dep = Department(name=department.name, 
                    id_organisation=department.id_organisation, 
                    description=department.description)
    session.add(dep)
    await session.commit()
    await session.refresh(dep)

    return dep

@router.patch("/update_department/{dep_id}", response_model=Department, status_code=200)
async def update_department(dep_id: int, department: DepartmentUpdate, session: AsyncSession = Depends(get_session)):
    await session.execute("UPDATE department SET name = '{0}', id_organisation = '{1}', "
                                                "description = '{2}'  WHERE id = {3}"
                                                .format(department.name, department.id_organisation, 
                                                department.description, dep_id))
    await session.commit()
    return department


@router.delete("/delete_department/{dep_id}")
async def delete_department(dep_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute("DELETE FROM department where id = {}".format(dep_id))
    await session.commit()
    return 'OK'
