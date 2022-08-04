from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import get_session
from app.models.employee import Employee, EmployeeCreate, EmployeeUpdate, EmployeeReadWithPersonandDepartment
from app.models.department import Department, DepartmentCreate, DepartmentUpdate
from app.models.person import Person, PersonCreate, PersonUpdate
from sqlalchemy.orm import selectinload

app = FastAPI()


@app.get("/api/employees", response_model=list[EmployeeReadWithPersonandDepartment])
async def get_employees(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Employee).options(selectinload('*')))
    empls = result.scalars().all()

    return [empl for empl in empls]


@app.post("/api/employees", status_code=200)
async def add_employee(empl: EmployeeCreate, session: AsyncSession = Depends(get_session)):
    empl = Employee(id=empl.id,
                    tab=empl.tab, 
                    id_person=empl.id_person, 
                    id_department=empl.id_department) 
    session.add(empl)
    await session.commit()
    await session.refresh(empl)
    return empl


@app.patch("/api/employees/{empl_id}", status_code=200)
async def update_employee(empl_id: int, employee: EmployeeUpdate, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    req = await request.json()
    exists = await session.execute(select(Employee).where(Employee.id == empl_id))
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        res = await session.execute("UPDATE employee SET tab = '{0}', hire_date = '{1}', dismissal_date = '{2}' WHERE id = {3}"
                                                    .format(req['tab'], req['hire_date'], req['dismissal_date'], empl_id))
        await session.commit()
        return 'OK'


@app.delete("/api/employees/{empl_id}")
async def delete_employee(empl_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute("DELETE FROM employee where id = {}".format(empl_id))
    await session.commit()
    return 'OK'


@app.get("/api/persons", response_model=list[Person])
async def get_persons(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Person).options(selectinload('*')))
    persons = result.scalars().all()

    return [person for person in persons]


@app.post("/api/persons", status_code=200)
async def add_person(person: Person, session: AsyncSession = Depends(get_session)):
    res = Person(first_name=person.first_name, 
                    last_name=person.last_name, 
                    birthday=person.birthday,
                    address=person.address) 
    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res


@app.patch("/api/persons/{person_id}", status_code=200)
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


@app.delete("/api/persons/{person_id}")
async def delete_employee(person_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute("DELETE FROM person where id = {}".format(person_id))
    await session.commit()
    return res


@app.get("/api/departments", response_model=list[Department])
async def get_departments(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Department).options(selectinload('*')))
    persons = result.scalars().all()

    return [person for person in persons]


@app.post("/api/departments", status_code=200)
async def add_department(department: DepartmentCreate, session: AsyncSession = Depends(get_session)):
    res = Department(name=department.name, 
                    id_organisation=department.id_organisation, 
                    description=department.description) 
    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res


@app.patch("/api/departments/{dep_id}", status_code=200)
async def update_department(empl_id: int, employee: DepartmentUpdate, request: Request,
                                            session: AsyncSession = Depends(get_session)):
    req = await request.json()
    exists = await session.execute(select(Department).where(Department.id == empl_id))
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")
    else:
        res = await session.execute("UPDATE department SET description = '{0}' WHERE id = {1}"
                                                    .format(req['description'], empl_id))
        await session.commit()
        return 'OK'


@app.delete("/api/departments/{dep_id}", status_code=200)
async def delete_department(dep_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute("DELETE FROM department where id = {}".format(dep_id))
    await session.commit()
    return res

