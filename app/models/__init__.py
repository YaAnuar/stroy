from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from sqlalchemy import UniqueConstraint, Column, Integer
from datetime import date