from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    description: Optional[str] = None
    category: Optional[str] = None


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    completed: bool
    category: Optional[str]
    created_at: datetime
