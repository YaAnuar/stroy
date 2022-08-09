from urllib import response
from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException
from app.models.employee import EmployeeBase, Employee, EmployeeCreate, EmployeeUpdate, EmployeeReadAll

router = APIRouter(
    prefix="/api",
    tags=["employees"]
)

@router.get("/get_list_employees/", response_model=list[EmployeeReadAll])
async def get_list_employees(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Employee).options(selectinload('*')))
    empls = result.scalars().all()   
    return empls


@router.get("/get_employee_by_id/{empl_id}", response_model=EmployeeReadAll)
async def get_employee_by_id(empl_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Employee).where(Employee.id == empl_id).options(selectinload('*')))
    empl = result.scalars().one()

    return empl


@router.post("/create_employee", response_model=Employee)
async def create_person(employee: EmployeeCreate, session: AsyncSession = Depends(get_session)):
    employee_dict = employee.dict()
    employee = Employee(**employee_dict)
    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    return employee 




@router.patch("/update_employee/{empl_id}", response_model=Employee)
async def update_employee(empl_id: int, empolyee: EmployeeUpdate, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Employee).where(Employee.id == empl_id))
    exists = res.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        res = await session.get(Employee, empl_id)
        empolyee_data = empolyee.dict(exclude_unset=True)
        for key, value in empolyee_data.items():
            setattr(res, key, value)
        await session.commit()
        return empolyee

@router.delete("/delete_employee/{empl_id}")
async def delete_employee(empl_id: int, session: AsyncSession = Depends(get_session)):
    employee = await session.get(Employee, empl_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await session.delete(employee)
    await session.commit()
    return {"ok": True}
