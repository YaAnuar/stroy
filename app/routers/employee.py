from app.routers import AsyncSession, get_session, select, Depends, selectinload, Request, APIRouter
from app.routers import HTTPException, ValidationError
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


@router.get("/get_employee_by_id/{empl_id}", response_model=list[EmployeeReadAll])
async def get_employee_by_id(empl_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Employee).where(Employee.id == empl_id).options(selectinload('*')))
    empls = result.scalars().all()

    return empls



@router.post("/add_employee/")
async def add_employee(request: Request, session: AsyncSession = Depends(get_session)):
    req = await request.json()
    try:
        if {'tab', 'hire_date', 'dismissal_date', 'id_person', 'id_department'} <= set(req):
            Employee_validate(req)
        else:
            return  HTTPException(status_code=400, detail="Missed request value.")
    except ValidationError as e:
        return  HTTPException(status_code=400, detail="Incorrect values: " + str(e))
    else:
        empl = Employee(tab=req['tab'], 
                        hire_data=req['hire_date'],
                        dismissal_date=req['dismissal_date'],
                        id_person=req['id_person'], 
                        id_department=req['id_department'])
        session.add(empl)
        await session.commit()
        await session.refresh(empl)

        return empl


@router.patch("/update_employee/{empl_id}")
async def update_employee(empl_id: int, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Employee).where(Employee.id == empl_id))
    exists = res.scalars().all()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        req = await request.json()
        try:
            if {'tab', 'hire_date', 'dismissal_date', 'id_person', 'id_department'} <= set(req):
                Employee_validate(req)
            else:
                return  HTTPException(status_code=400, detail="Missed request value.")
        except ValidationError as e:
            return  HTTPException(status_code=400, detail="Incorrect values: " + str(e))
        else:
            await session.execute("UPDATE employee SET tab = '{0}', hire_date = '{1}', dismissal_date = '{2}',"
                                                "id_person = '{3}', id_department = '{4}'"
                                                " WHERE id = {5}"
                                                    .format(req['tab'], req['hire_date'], req['dismissal_date'], 
                                                req['id_person'], req['id_department'], req['empl_id']))
            await session.commit()

            return 'OK'

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
