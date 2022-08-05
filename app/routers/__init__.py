from fastapi import FastAPI, Request, Depends, APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.config.db import get_session
from fastapi.exceptions import HTTPException
from pydantic import ValidationError