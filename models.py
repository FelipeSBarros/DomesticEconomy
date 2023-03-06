import os

from dotenv import load_dotenv
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)


class Base(DeclarativeBase):
    pass


class General(Base):
    __tablename__ = "general"

    id: Mapped[int] = mapped_column(primary_key=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"))
    action: Mapped[
        "Action"
    ] = (
        relationship()
    )  # back_populates="Action", cascade="all, delete-orphan")  # todo not sure if should use
    user: Mapped[int] = mapped_column(ForeignKey("user.id"))
    category: Mapped[int] = mapped_column(ForeignKey("category.id"))
    subcategory: Mapped[int] = mapped_column(ForeignKey("subcategory.id"))
    value: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_al: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"Genetal(id={self.id}, action_id={self.action.name}"


class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))  # todo mudar de action para name

    def __repr__(self) -> str:
        return f"Action(id={self.id}, action={self.name})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))  # todo change in the code from 'user'
    chat_id: Mapped[str] = mapped_column(
        String(30)
    )  # todo change in the code from 'chat'


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(30)
    )  # todo change in the code from 'category'


class Subcategory(Base):
    __tablename__ = "subcategory"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    name: Mapped[str] = mapped_column(
        String(30)
    )  # todo change in the code from 'subcategory'
