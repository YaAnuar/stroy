from urllib import response
from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException
from app.models.employee import EmployeeBase, Employee, EmployeeCreate, EmployeeUpdate, EmployeeReadAll, Employee_validate

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



@router.post("/create_employee/", response_model=Employee)
async def create_employee(empolyee: EmployeeCreate, session: AsyncSession = Depends(get_session)):
    empl = Employee(tab=empolyee.tab, 
                    hire_date=empolyee.hire_date,
                    dismissal_date=empolyee.dismissal_date,
                    id_person=empolyee.id_person, 
                    id_department=empolyee.id_department)
    session.add(empl)
    await session.commit()
    await session.refresh(empl)

    return empl


@router.patch("/update_employee/{empl_id}", response_model=Employee)
async def update_employee_by_id(empl_id: int, empolyee: EmployeeUpdate, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Employee).where(Employee.id == empl_id))
    exists = res.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        await session.execute("UPDATE employee SET tab = '{0}', hire_date = '{1}', dismissal_date = '{2}',"
                                            "id_person = '{3}', id_department = '{4}'"
                                            " WHERE id = {5}"
                                                .format(empolyee.tab, empolyee.hire_date, empolyee.dismissal_date, 
                                            empolyee.id_person, empolyee.id_department, empl_id))
        await session.commit()

        return empolyee

@router.delete("/delete_employee/{empl_id}")
async def delete_employee(empl_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Employee).where(Employee.id == empl_id))
    exists = res.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        await session.execute("DELETE FROM employee where id = {}".format(empl_id))
        await session.commit()
        
        return 'OK'
