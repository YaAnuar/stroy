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
    department_dict = department.dict()
    department = Department(**department_dict)
    session.add(department)
    await session.commit()
    await session.refresh(department)

    return department


@router.patch("/update_department/{dep_id}", response_model=DepartmentUpdate, status_code=200)
async def update_department(dep_id: int, department: DepartmentUpdate, session: AsyncSession = Depends(get_session)):
    exists = await session.execute(select(Department).where( Department.id == dep_id ))
    exists = exists.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Department not found")
    else:
        res = await session.get(Department, dep_id)
        department_data = department.dict(exclude_unset=True)
        for key, value in department_data.items():
            setattr(res, key, value)
        await session.commit()
        return department


@router.delete("/delete_department/{dep_id}")
async def delete_department(dep_id: int, session: AsyncSession = Depends(get_session)):
    department = await session.get(Department, dep_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    await session.delete(department)
    await session.commit()
    return {"ok": True}
